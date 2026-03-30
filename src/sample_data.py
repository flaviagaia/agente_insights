from __future__ import annotations

from pathlib import Path

import pandas as pd


RAW_DIR = Path(__file__).resolve().parents[1] / "data" / "raw"
SNAPSHOT_PATH = RAW_DIR / "business_snapshots.csv"


DEFAULT_SNAPSHOTS = [
    {
        "company_id": "BIZ-1001",
        "company_name": "NovaOps",
        "sector": "B2B SaaS",
        "period": "2026-Q1",
        "revenue_current": 1250000,
        "revenue_previous": 1080000,
        "gross_margin_pct": 71.4,
        "active_customers": 415,
        "new_customers": 52,
        "churn_pct": 4.8,
        "nps": 46,
        "marketing_cac": 860,
        "support_tickets": 920,
        "on_time_delivery_pct": 95.2,
        "inventory_turnover": 0.0,
        "notes": "Expansão comercial forte, mas aumento de tickets de onboarding.",
    },
    {
        "company_id": "BIZ-1002",
        "company_name": "RetailPulse",
        "sector": "Retail Analytics",
        "period": "2026-Q1",
        "revenue_current": 840000,
        "revenue_previous": 865000,
        "gross_margin_pct": 58.1,
        "active_customers": 288,
        "new_customers": 21,
        "churn_pct": 7.2,
        "nps": 31,
        "marketing_cac": 1120,
        "support_tickets": 710,
        "on_time_delivery_pct": 89.4,
        "inventory_turnover": 0.0,
        "notes": "Queda moderada de receita e churn pressionado por concorrência com menor preço.",
    },
    {
        "company_id": "BIZ-1003",
        "company_name": "LogiChain",
        "sector": "Supply Chain Tech",
        "period": "2026-Q1",
        "revenue_current": 2140000,
        "revenue_previous": 1995000,
        "gross_margin_pct": 49.7,
        "active_customers": 164,
        "new_customers": 13,
        "churn_pct": 2.1,
        "nps": 54,
        "marketing_cac": 2410,
        "support_tickets": 380,
        "on_time_delivery_pct": 87.1,
        "inventory_turnover": 4.9,
        "notes": "Receita cresce, mas margem e eficiência operacional merecem atenção.",
    },
]


def ensure_sample_data() -> pd.DataFrame:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    if not SNAPSHOT_PATH.exists():
        pd.DataFrame(DEFAULT_SNAPSHOTS).to_csv(SNAPSHOT_PATH, index=False)
    return pd.read_csv(SNAPSHOT_PATH)


def load_snapshots() -> pd.DataFrame:
    return ensure_sample_data()


def load_snapshot(company_id: str) -> dict:
    snapshots = ensure_sample_data()
    match = snapshots.loc[snapshots["company_id"] == company_id]
    if match.empty:
        raise KeyError(f"Company id not found: {company_id}")
    return match.iloc[0].to_dict()
