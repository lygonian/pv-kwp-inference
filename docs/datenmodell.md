# Datenmodell

## `invoice_positions.csv`

| Spalte | Bedeutung |
| --- | --- |
| `project_id` | Synthetische Projekt-ID. |
| `invoice_number` | Synthetische Rechnungsnummer. |
| `line_id` | Positionsnummer. |
| `position_title` | Synthetischer Positionstitel. |
| `quantity` | Menge. |
| `unit` | Einheit. |
| `watt_peak` | Watt-Peak je Modul, falls vorhanden. |
| `montage_kwp` | Optionaler Montage-Fallback. |
| `offer_kwp` | Optionaler Angebots-Fallback. |

## Prioritaet

1. PV-Modulzeilen: `quantity * watt_peak / 1000`.
2. Montage-kWp, wertdedupliziert.
3. Angebots-kWp, groesster positiver Wert.
4. Explizit `missing`, wenn kein Signal vorhanden ist.
