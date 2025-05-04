import json
from typing import List, Dict, Any, Optional
import os
import numpy as np
import pandas as pd
import torch
from sentence_transformers import SentenceTransformer
from user_profiler import generate_user_profile_summary, calculate_potential_savings

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

torch.classes.__path__ = []

class _ModelCache:
    _model: Optional[SentenceTransformer] = None

    @classmethod
    def get(cls) -> SentenceTransformer:
        if cls._model is None:
            cls._model = SentenceTransformer(MODEL_NAME)
        return cls._model

def _embed(texts: List[str]) -> np.ndarray:
    model = _ModelCache.get()
    return model.encode(texts, normalize_embeddings=True)

def _load_vendors(path: str) -> List[Dict[str, Any]]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def _vendor_embeddings(vendors: List[Dict[str, Any]]) -> np.ndarray:
    blobs = [
        " | ".join([
            v["vendor_name"],
            v.get("category", ""),
            v["offer_details"].get("offer_description", ""),
            " ".join(v.get("tags", [])),
        ])
        for v in vendors
    ]
    return _embed(blobs)

def _choose_anchor_vendors(
    txn_df: pd.DataFrame, k: int = 5, tau_days: int = 3
) -> List[Dict[str, str]]:
    if "timestamp" not in txn_df.columns:
        raise ValueError("txn_df must include a 'timestamp' column parsed as datetime")
    max_ts = txn_df["timestamp"].max()
    txn_df = txn_df.copy()
    txn_df["recency_weight"] = np.exp(-(max_ts - txn_df["timestamp"]).dt.days / tau_days)
    txn_df["weighted_amount"] = txn_df["recency_weight"] * txn_df["amount"].abs()
    stats = txn_df.groupby(["merchant_name", "category"]).agg(
        freq=("recency_weight", "sum"), spend=("weighted_amount", "sum")
    ).reset_index()
    freq_norm = stats["freq"] / stats["freq"].max()
    spend_norm = stats["spend"] / stats["spend"].max()
    stats["score"] = 0.6 * freq_norm + 0.4 * spend_norm
    anchors, seen_categories = [], set()
    for _, row in stats.sort_values("score", ascending=False).iterrows():
        if row["category"] in seen_categories:
            continue
        anchors.append({"merchant": row["merchant_name"], "category": row["category"]})
        seen_categories.add(row["category"])
        if len(anchors) == k:
            break
    return anchors

def _score_vendors(
    anchor: Dict[str, str],
    vendors: List[Dict[str, Any]],
    vendor_vecs: np.ndarray,
    user_summary: Dict[str, Any],
    txn_df: pd.DataFrame,
    category_filter: Optional[str] = None,
) -> List[tuple[float, str, str, str]]:
    anchor_blob = f"{anchor['merchant']} | {anchor['category']}"
    anchor_vec = _embed([anchor_blob])[0]
    purchased = set(txn_df["merchant_name"].unique())
    avg_spend = user_summary.get("avg_spend_per_category", {})
    results = []
    for idx, vendor in enumerate(vendors):
        if vendor["vendor_name"].lower() == anchor["merchant"].lower():
            continue
        if category_filter and vendor.get("category") != category_filter:
            continue
        sim = float(np.dot(anchor_vec, vendor_vecs[idx]))
        est_value = calculate_potential_savings(vendor["offer_details"], avg_spend)
        cat_avg = avg_spend.get(vendor.get("category", ""), 1.0)
        value_norm = min(est_value / cat_avg, 1.0) if cat_avg else 0.0
        novelty = 0.0 if vendor["vendor_name"] in purchased else 1.0
        score = 0.6 * sim + 0.25 * value_norm + 0.15 * novelty
        otype = vendor["offer_details"].get("offer_type", "")
        results.append((score, vendor["vendor_id"], vendor["vendor_name"], otype))
    return results

def _diverse_top_vendors(
    scores: List[tuple[float, str, str, str]], top_n: int
) -> List[Dict[str, str]]:
    from collections import defaultdict
    scores.sort(key=lambda x: x[0], reverse=True)
    groups = defaultdict(list)
    for sc, vid, vname, otype in scores:
        groups[otype].append((sc, vid, vname))
    ordered_types = sorted(groups.keys(), key=lambda t: groups[t][0][0], reverse=True)
    results = []
    while len(results) < top_n and any(groups.values()):
        for otype in ordered_types:
            if not groups[otype]:
                continue
            _sc, vid, vname = groups[otype].pop(0)
            if any(r["vendor_id"] == vid for r in results):
                continue
            results.append({"vendor_id": vid, "vendor_name": vname})
            if len(results) == top_n:
                break
    return results

def _recommend_for_anchor(
    anchor: Dict[str, str],
    vendors: List[Dict[str, Any]],
    vendor_vecs: np.ndarray,
    user_summary: Dict[str, Any],
    txn_df: pd.DataFrame,
    top_n: int = 6,
) -> List[Dict[str, str]]:
    scores = _score_vendors(anchor, vendors, vendor_vecs, user_summary, txn_df, anchor["category"])
    if len(scores) < top_n:
        scores = _score_vendors(anchor, vendors, vendor_vecs, user_summary, txn_df, None)
    return _diverse_top_vendors(scores, top_n)

def generate_recs(
    vendor_path: str = "../data/partner_vendors.json",
    transactions_path: str = "../data/final_data.csv",
    analysis_timeframe_days: int = 30,
    k_panels: int = 3,
    panel_size: int = 6,
    exclude_last_n: int = 0,
) -> List[Dict[str, Any]]:
    """
    Generate recommendation panels for the front-end.
    exclude_last_n: Exclude the most recent n transactions from analysis.
    Returns a list of dicts: {reason, anchor_merchant, category, offers}
    """
    txn_df = pd.read_csv(
        transactions_path,
        usecols=["timestamp", "merchant_name", "category", "amount"],
        parse_dates=["timestamp"],
    ).sort_values("timestamp", ascending=False).reset_index(drop=True)
    if exclude_last_n > 0 and len(txn_df) > exclude_last_n:
        txn_df = txn_df.iloc[exclude_last_n:].copy()
    temp_path = None
    if exclude_last_n > 0 and len(txn_df) > 0:
        import tempfile
        temp = tempfile.NamedTemporaryFile(delete=False, suffix=".csv")
        txn_df.to_csv(temp.name, index=False)
        temp_path = temp.name
        temp.close()
        summary = generate_user_profile_summary(
            path=temp_path, analysis_timeframe_days=analysis_timeframe_days
        )
        os.unlink(temp_path)
    else:
        summary = generate_user_profile_summary(
            path=transactions_path, analysis_timeframe_days=analysis_timeframe_days
        )
    vendors = _load_vendors(vendor_path)
    vendor_vecs = _vendor_embeddings(vendors)
    anchors = _choose_anchor_vendors(txn_df, k=k_panels)
    panels = []
    for anchor in anchors:
        offers = _recommend_for_anchor(
            anchor, vendors, vendor_vecs, summary, txn_df, top_n=panel_size
        )
        panels.append(
            {
                "reason": f"Because you bought at {anchor['merchant']}",
                "anchor_merchant": anchor["merchant"],
                "category": anchor["category"],
                "offers": offers,
            }
        )
    return panels

if __name__ == "__main__":
    import pprint
    p = generate_recs()
    pprint.pp(p) 