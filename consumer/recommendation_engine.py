import json
from typing import List, Dict, Any, Optional

import numpy as np
import pandas as pd
import torch

from sentence_transformers import SentenceTransformer

# Re-use data processing & valuation helpers from the existing module
from user_profiler import (
    generate_user_profile_summary,
    calculate_potential_savings,
)

torch.classes.__path__ = []


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


class _ModelCache:
    """Singleton-ish cache so we only load the encoder once."""

    _model: Optional[SentenceTransformer] = None

    @classmethod
    def get(cls) -> SentenceTransformer:
        if cls._model is None:
            cls._model = SentenceTransformer(MODEL_NAME)
        return cls._model


def _embed(texts: List[str]) -> np.ndarray:
    """Helper that encodes *and* returns normalised vectors."""
    model = _ModelCache.get()
    vectors = model.encode(texts, normalize_embeddings=True)
    return vectors


# ---------------------------------------------------------------------------
#                               Vendor helpers
# ---------------------------------------------------------------------------

def _load_vendors(path: str) -> List[Dict[str, Any]]:
    """Load newline-delimited JSON (JSONL) vendor dump."""
    vendors: List[Dict[str, Any]] = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            vendors.append(json.loads(line))
    return vendors


def _build_vendor_embeddings(vendors: List[Dict[str, Any]]) -> np.ndarray:
    """Vectorise each vendor once. Returns an (N, dim) matrix."""
    blobs = [
        " | ".join(
            [
                v["vendor_name"],
                v.get("category", ""),
                v["offer_details"].get("offer_description", ""),
                " ".join(v.get("tags", [])),
            ]
        )
        for v in vendors
    ]
    return _embed(blobs)


# ---------------------------------------------------------------------------
#                           Anchor (panel) selection
# ---------------------------------------------------------------------------

def _choose_anchor_vendors(txn_df: pd.DataFrame, k: int = 5, tau_days: int = 14) -> List[Dict[str, str]]:
    """Pick *k* distinct-category vendors with an exponential recency bias.

    Transactions are weighted by   exp(-Δdays / tau_days)  before computing
    per-merchant frequency and spend aggregates so that recent activity matters
    more than older history.
    """

    if "timestamp" not in txn_df.columns:
        raise ValueError("txn_df must include a 'timestamp' column parsed as datetime")

    max_ts = txn_df["timestamp"].max()
    # Exponential decay weight
    txn_df = txn_df.copy()
    txn_df["recency_weight"] = np.exp(-(max_ts - txn_df["timestamp"]).dt.days / tau_days)

    # Frequency: sum of weights; Spend: weight * abs(amount)
    txn_df["weighted_amount"] = txn_df["recency_weight"] * txn_df["amount"].abs()

    stats = (
        txn_df.groupby(["merchant_name", "category"]).agg(
            freq=("recency_weight", "sum"), spend=("weighted_amount", "sum")
        ).reset_index()
    )

    # Normalise & combine into a score
    freq_norm = stats["freq"] / stats["freq"].max()
    spend_norm = stats["spend"] / stats["spend"].max()
    stats["score"] = 0.6 * freq_norm + 0.4 * spend_norm

    anchors: List[Dict[str, str]] = []
    seen_categories: set[str] = set()
    for _, row in stats.sort_values("score", ascending=False).iterrows():
        if row["category"] in seen_categories:
            continue
        anchors.append({"merchant": row["merchant_name"], "category": row["category"]})
        seen_categories.add(row["category"])
        if len(anchors) == k:
            break
    return anchors


# ---------------------------------------------------------------------------
#                            Panel-level recommend
# ---------------------------------------------------------------------------

def _recommend_for_anchor(
    anchor: Dict[str, str],
    vendors: List[Dict[str, Any]],
    vendor_vecs: np.ndarray,
    user_summary: Dict[str, Any],
    txn_df: pd.DataFrame,
    top_n: int = 6,
) -> List[Dict[str, str]]:
    """Return *top_n* vendor_ids for the given anchor vendor."""
    # Build anchor text and vector
    anchor_blob = f"{anchor['merchant']} | {anchor['category']}"
    anchor_vec = _embed([anchor_blob])[0]  # single vector

    # quick look-up sets / maps
    purchased_merchants = set(txn_df["merchant_name"].unique())
    avg_spend_map = user_summary.get("avg_spend_per_category", {})

    def _collect_scores(category_filter: Optional[str] = None) -> List[tuple[float, str, str]]:
        collected: List[tuple[float, str, str]] = []
        for idx, vendor in enumerate(vendors):
            if vendor["vendor_name"].lower() == anchor["merchant"].lower():
                continue
            if category_filter and vendor.get("category") != category_filter:
                continue

            sim = float(np.dot(anchor_vec, vendor_vecs[idx]))
            est_value = calculate_potential_savings(vendor["offer_details"], avg_spend_map)
            cat_avg = avg_spend_map.get(vendor.get("category", ""), 1.0)
            value_norm = min(est_value / cat_avg, 1.0) if cat_avg else 0.0
            novelty = 0.0 if vendor["vendor_name"] in purchased_merchants else 1.0
            score = 0.6 * sim + 0.3 * value_norm + 0.1 * novelty
            collected.append((score, vendor["vendor_id"], vendor["vendor_name"]))
        return collected

    # First attempt: only same category as anchor
    scores = _collect_scores(anchor["category"])
    # Fallback if not enough
    if len(scores) < top_n:
        scores = _collect_scores(None)

    scores.sort(key=lambda x: x[0], reverse=True)
    results: List[Dict[str, str]] = []
    for _, vid, vname in scores[:top_n]:
        results.append({"vendor_id": vid, "vendor_name": vname})
    return results


# ---------------------------------------------------------------------------
#                           Public entry point
# ---------------------------------------------------------------------------

def generate_recs(
    vendor_path: str = "../data/partner_vendors_with_tags_4o.jsonl",
    transactions_path: str = "../data/final_data.csv",
    analysis_timeframe_days: int = 30,
    k_panels: int = 3,
    panel_size: int = 6,
) -> List[Dict[str, Any]]:
    """End-to-end pipeline returning panels consumable by the front-end.

    Returns
    -------
    list[dict]
        Each dict has keys: reason, anchor_merchant, category, offers (list[str])
    """
    # 1. User summary
    summary = generate_user_profile_summary(
        path=transactions_path, analysis_timeframe_days=analysis_timeframe_days
    )

    # 2. Raw user transactions (to pick anchors, novelty, etc.)
    txn_df = pd.read_csv(
        transactions_path,
        usecols=["timestamp", "merchant_name", "category", "amount"],
        parse_dates=["timestamp"],
    )

    vendors = _load_vendors(vendor_path)
    vendor_vecs = _build_vendor_embeddings(vendors)

    # 3. Anchors → distinct categories
    anchors = _choose_anchor_vendors(txn_df, k=k_panels)

    # 4. Build panels
    panels: List[Dict[str, Any]] = []
    for anchor in anchors:
        offer_entries = _recommend_for_anchor(
            anchor,
            vendors,
            vendor_vecs,
            summary,
            txn_df,
            top_n=panel_size,
        )
        panels.append(
            {
                "reason": f"Because you bought at {anchor['merchant']}",
                "anchor_merchant": anchor["merchant"],
                "category": anchor["category"],
                "offers": offer_entries,
            }
        )

    return panels


if __name__ == "__main__":
    # quick manual test – prints three panels
    import pprint

    p = generate_recs()
    pprint.pp(p) 