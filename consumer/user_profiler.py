import json
from typing import Dict, Any, List, Optional

import pandas as pd

def generate_user_profile_summary(
    path="../data/final_data.csv",
    analysis_timeframe_days: int = 30,
    top_n_categories: int = 3,
    top_n_merchants: int = 5,
) -> dict:
    """
    Produce a JSON serializable profile summary from raw transactions.

    Args:
        df: DataFrame with columns ['timestamp', 'merchant_name', 'category', 'amount'].
        analysis_timeframe_days: lookback window (days) from the latest timestamp in df.
        top_n_categories: how many top categories by frequency to include.
        top_n_merchants: how many merchants by frequency to include.

    Returns:
        {
            'analysis_timeframe_days': int,
            'top_categories': [
              {'category': str, 'frequency_rank': int, 'spend_rank': int}, …
            ],
            'frequent_merchants': [
              {'merchant': str, 'category': str}, …
            ],
            'avg_spend_per_category': {category: float, …},
            'spending_velocity': avg_txns_per_day,
            'typical_spending_times': [str, …]
        }
    """
    df = pd.read_csv(path, usecols=["timestamp","merchant_name","category","amount"], parse_dates=True, index_col=0).reset_index()
    df['amount'] = -df['amount']

    # 1) Ensure timestamp dtype and copy
    df = df.copy()
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # 2) Filter to the last N days
    max_ts = df['timestamp'].max()
    cutoff = max_ts - pd.Timedelta(days=analysis_timeframe_days)
    df = df[df['timestamp'] >= cutoff]
    if df.empty:
        raise ValueError("No transactions in the specified timeframe")

    # 3) Top Categories by frequency & spend
    cat_stats = (
        df.groupby('category')
          .agg(frequency=('category','size'), total_spend=('amount','sum'))
    )
    # assign dense ranks (1 = highest)
    cat_stats['frequency_rank'] = cat_stats['frequency'] \
        .rank(method='dense', ascending=False).astype(int)
    cat_stats['spend_rank'] = cat_stats['total_spend'] \
        .rank(method='dense', ascending=False).astype(int)

    # select top N by frequency
    top = cat_stats.sort_values('frequency', ascending=False).head(top_n_categories)
    top_categories = [
        {
            'category': cat,
            'frequency_rank': int(row.frequency_rank),
            'spend_rank': int(row.spend_rank)
        }
        for cat, row in top.iterrows()
    ]

    # 4) Frequent merchants (by count)
    merch = (
        df.groupby(['merchant_name','category'])
          .size()
          .reset_index(name='count')
          .sort_values('count', ascending=False)
          .head(top_n_merchants)
    )
    frequent_merchants = [
        {'merchant': r.merchant_name, 'category': r.category}
        for _, r in merch.iterrows()
    ]

    # 5) Average spend per category
    avg_spend_per_category = (
        df.groupby('category')['amount']
          .mean()
          .round(2)
          .to_dict()
    )

    # 6) Spending velocity: avg txns/day → low/medium/high
    days = max(1, (max_ts - cutoff).days)
    avg_txns_per_day = len(df) / days

    # 7) Typical spending times
    #    bucket hours into morning/afternoon/evening/night
    def bucket(h):
        if 5 <= h <= 11:   return 'morning'
        if 12 <= h <= 17:  return 'afternoon'
        if 18 <= h <= 21:  return 'evening'
        return 'night'

    df['hour'] = df['timestamp'].dt.hour
    df['time_bucket'] = df['hour'].apply(bucket)
    df['day_type'] = df['timestamp'].dt.weekday \
        .apply(lambda x: 'weekday' if x < 5 else 'weekend')

    combo = (
        df.groupby(['day_type','time_bucket'])
          .size()
          .reset_index(name='count')
          .sort_values('count', ascending=False)
          .head(2)
    )
    typical_spending_times = [
        f"{r.day_type} {r.time_bucket}s"
        for _, r in combo.iterrows()
    ]

    return {
        'analysis_timeframe_days': analysis_timeframe_days,
        'top_categories': top_categories,
        'frequent_merchants': frequent_merchants,
        'avg_spend_per_category': avg_spend_per_category,
        'spending_velocity': round(avg_txns_per_day, 1),
        'typical_spending_times': typical_spending_times
    }

def filter_vendors_by_category(categories: list[str], path: str = "../data/partner_vendors.json"):
    with open(path) as f:
        vendors = json.load(f)
    return [vendor for vendor in vendors if vendor["category"] in categories]


def compare_offer_relevance(
    offer_category: str,
    user_top_categories: List[Dict[str, Any]],
    similarity_fn: Optional[Any] = None
) -> float:
    """
    Compute a relevance score based on whether the offer category appears
    in the user's top categories or is similar to them.

    Args:
      offer_category: category string of the offer.
      user_top_categories: list of dicts with key 'category'.
      similarity_fn: optional function that takes (offer_category, top_category)
        and returns a similarity score in [0,1].

    Returns:
      relevance score in [0.0, 1.0].
    """
    top_cats = {entry['category'] for entry in user_top_categories}
    # Exact match
    if offer_category in top_cats:
        return 1.0

    # Fallback: similarity check (e.g. taxonomy or embedding-based)
    if similarity_fn:
        scores = [similarity_fn(offer_category, c) for c in top_cats]
        max_sim = max(scores, default=0.0)
        return max_sim * 0.8  # downweight similarity vs exact

    # Default no relevance
    return 0.0


def calculate_potential_savings(
    offer_details: Dict[str, Any],
    avg_spend_per_category: Dict[str, float],
    lookup_price_fn: Optional[Any] = None
) -> float:
    """
    Estimate the cash-equivalent savings of an offer for a representative user.

    Args:
      offer_details: dict with keys:
        - offer_type: one of [percentage_discount, fixed_discount,
          points_for_cash, free_item, buy_one_get_one]
        - offer_value: numeric (percent or absolute)
        - points_cost: optional, for points_for_cash
        - item_category: optional, for free_item or buy_one_get_one
      avg_spend_per_category: map from category to average spend per use.
      lookup_price_fn: optional function to fetch average item price by category.

    Returns:
      estimated savings per use in same currency as avg_spend.
    """
    otype = offer_details.get('offer_type')
    value = offer_details.get('offer_value', 0)
    category = offer_details.get('category')
    avg_spend = avg_spend_per_category.get(category, 0.0)

    if otype == 'percentage_discount':
        # e.g. 15% off a €8 coffee
        return avg_spend * (value / 100.0)

    elif otype in ('fixed_discount', 'fixed_voucher'):
        # e.g. €5 off
        # cap at avg_spend so we don't over-credit
        return min(value, avg_spend)

    elif otype == 'points_for_cash':
        # e.g. 500 points -> €5 credit
        return float(value)

    elif otype == 'free_item':
        # e.g. free coffee
        # Estimate via lookup_price_fn or fallback to avg_spend
        if lookup_price_fn and 'item_category' in offer_details:
            return lookup_price_fn(offer_details['item_category'])
        return avg_spend

    elif otype == 'buy_one_get_one':
        # e.g. 2-for-1 cinema ticket
        if lookup_price_fn and 'item_category' in offer_details:
            return lookup_price_fn(offer_details['item_category'])
        return avg_spend

    # Unknown type
    return 0.0


def evaluate_offer(
    vendor: Dict[str, Any],
    user_summary: Dict[str, Any],
    similarity_fn: Optional[Any] = None,
    lookup_price_fn: Optional[Any] = None
) -> Dict[str, Any]:
    """
    Orchestrates relevance & savings calculation, returns evaluation.

    Returns a dict:
      {
        'offer_id': str,
        'relevance_score': float,
        'estimated_value': float,
        'notes': str
      }
    """
    details = vendor['offer_details']
    offer_cat = vendor.get('category')
    top_cats = user_summary.get('top_categories', [])

    # 1. Compute relevance
    relevance = compare_offer_relevance(
        offer_cat,
        top_cats,
        similarity_fn=similarity_fn
    )

    # 2. Compute savings
    avg_spends = user_summary.get('avg_spend_per_category', {})
    # flatten offer details for savings fn
    flat_offer = {
        'offer_type': details.get('offer_type'),
        'offer_value': details.get('offer_value'),
        'points_cost': details.get('points_cost'),
        'category': vendor.get('category'),
        'item_category': details.get('offer_description')  # could parse
    }
    savings = calculate_potential_savings(
        flat_offer,
        avg_spends,
        lookup_price_fn=lookup_price_fn
    )

    # 3. Combine into final structure
    result = {
        'offer_id': details.get('offer_id'),
        'relevance_score': relevance,
        'estimated_value': savings,
        # A simple templated note; you could replace this with an LLM call
        'notes': (
            f"This {flat_offer['offer_type'].replace('_',' ')} "
            f"saves about {savings:.2f} on a typical {offer_cat} purchase."
        )
    }

    # **LLM INTEGRATION POINT**:
    # To enhance 'notes', call your LLM here with a prompt like:
    # "User spends ~{avg_spends[offer_cat]:.2f} on {offer_cat}. Offer: {details}." 
    # and let it generate a persuasive 1-2 sentence description.

    return result

