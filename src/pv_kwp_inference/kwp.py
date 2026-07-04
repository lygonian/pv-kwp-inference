"""Infer installed PV capacity from synthetic invoice positions."""

from __future__ import annotations

import re

import pandas as pd

MODULE_EXCLUDE_TERMS = [
    "battery module",
    "internet module",
    "wifi module",
    "mixer module",
    "thermal solar",
]

KWP_COLUMNS = ["project_id", "kwp_final", "source", "invoice_numbers", "qa_note"]


def infer_project_kwp(positions: pd.DataFrame) -> pd.DataFrame:
    """Infer kWp per project using module rows before fallback values."""

    required = ["project_id", "invoice_number", "position_title", "quantity"]
    missing = [column for column in required if column not in positions.columns]
    if missing:
        raise ValueError(f"positions missing columns: {', '.join(missing)}")

    data = positions.copy()
    data["project_id"] = data["project_id"].astype("string").str.strip()
    data["invoice_number"] = data["invoice_number"].astype("string").str.upper().str.strip()
    data["position_title"] = data["position_title"].fillna("").astype(str)
    data["quantity"] = pd.to_numeric(data["quantity"], errors="coerce").fillna(0.0)
    for optional in ["watt_peak", "montage_kwp", "offer_kwp"]:
        if optional not in data.columns:
            data[optional] = pd.NA
        data[optional] = pd.to_numeric(data[optional], errors="coerce")

    rows: list[dict[str, object]] = []
    for project_id, group in data.groupby("project_id", dropna=False):
        invoice_numbers = ";".join(sorted(group["invoice_number"].dropna().unique()))
        module_kwp = _module_kwp(group)
        montage_values = _positive_unique(group["montage_kwp"])
        offer_values = _positive_unique(group["offer_kwp"])

        qa_note = ""
        if module_kwp > 0:
            kwp_final = module_kwp
            source = "module_rows"
            montage_total = sum(montage_values)
            if montage_total and abs(montage_total - module_kwp) / module_kwp > 0.02:
                qa_note = "module_vs_montage_diff"
        elif montage_values:
            kwp_final = sum(montage_values)
            source = "montage_fallback"
        elif offer_values:
            kwp_final = max(offer_values)
            source = "offer_fallback"
        else:
            kwp_final = 0.0
            source = "missing"
            qa_note = "no_capacity_signal"

        rows.append(
            {
                "project_id": project_id,
                "kwp_final": round(float(kwp_final), 3),
                "source": source,
                "invoice_numbers": invoice_numbers,
                "qa_note": qa_note,
            }
        )

    return pd.DataFrame(rows, columns=KWP_COLUMNS).sort_values("project_id").reset_index(drop=True)


def _module_kwp(group: pd.DataFrame) -> float:
    module_rows = group[group.apply(_is_pv_module_row, axis=1)].copy()
    if module_rows.empty:
        return 0.0
    return round(float((module_rows["quantity"] * module_rows["watt_peak"]).sum() / 1000), 3)


def _is_pv_module_row(row: pd.Series) -> bool:
    title = str(row["position_title"]).casefold()
    if "module" not in title:
        return False
    if any(term in title for term in MODULE_EXCLUDE_TERMS):
        return False
    watt_peak = row["watt_peak"]
    if pd.isna(watt_peak):
        match = re.search(r"\b([3-6]\d{2})\s*w(?:p|att)?\b", title)
        if not match:
            return False
        watt_peak = float(match.group(1))
    return 300 <= float(watt_peak) <= 700


def _positive_unique(series: pd.Series) -> list[float]:
    return sorted({round(float(value), 3) for value in series.dropna() if float(value) > 0})
