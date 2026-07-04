import pandas as pd

from pv_kwp_inference import infer_project_kwp


def test_module_rows_are_primary_and_battery_modules_are_excluded():
    positions = pd.DataFrame(
        [
            ("PV-1", "INV-1", "Solar module 450 W", 10, 450, 4.5, 4.5),
            ("PV-1", "INV-1", "Battery module 500 W", 1, 500, 4.5, 4.5),
        ],
        columns=["project_id", "invoice_number", "position_title", "quantity", "watt_peak", "montage_kwp", "offer_kwp"],
    )

    result = infer_project_kwp(positions).set_index("project_id")

    assert result.loc["PV-1", "kwp_final"] == 4.5
    assert result.loc["PV-1", "source"] == "module_rows"


def test_fallback_order_is_montage_then_offer():
    positions = pd.DataFrame(
        [
            ("PV-2", "INV-2", "Mounting rail", 1, None, 5.2, 5.8),
            ("PV-3", "INV-3", "Planning offer", 1, None, None, 6.4),
        ],
        columns=["project_id", "invoice_number", "position_title", "quantity", "watt_peak", "montage_kwp", "offer_kwp"],
    )

    result = infer_project_kwp(positions).set_index("project_id")

    assert result.loc["PV-2", "kwp_final"] == 5.2
    assert result.loc["PV-2", "source"] == "montage_fallback"
    assert result.loc["PV-3", "kwp_final"] == 6.4
    assert result.loc["PV-3", "source"] == "offer_fallback"


def test_missing_capacity_signal_is_explicit():
    positions = pd.DataFrame(
        [("OTHER-1", "INV-1", "Documentation", 1, None, None, None)],
        columns=["project_id", "invoice_number", "position_title", "quantity", "watt_peak", "montage_kwp", "offer_kwp"],
    )

    result = infer_project_kwp(positions).set_index("project_id")

    assert result.loc["OTHER-1", "kwp_final"] == 0
    assert result.loc["OTHER-1", "source"] == "missing"
    assert result.loc["OTHER-1", "qa_note"] == "no_capacity_signal"
