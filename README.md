# PV kWp Inference

Eigenstaendige, oeffentlich sichere Demo fuer die Ableitung installierter
PV-Leistung aus synthetischen Rechnungspositionen. Die Logik bevorzugt
physische Modulzeilen und nutzt Montage- oder Angebotswerte nur als Fallback.

Alle Daten sind synthetisch. Es sind keine echten Projekt-, Kunden-,
Rechnungs- oder Modulstammdaten enthalten.

## Funktionen

- PV-Modulzeilen erkennen.
- Nicht-PV-Module wie Batterie-/Internetmodule ausschliessen.
- kWp aus Menge mal Watt-Peak berechnen.
- Montage-kWp und Angebots-kWp als Fallback nutzen.
- QA-Hinweise fuer fehlende oder abweichende Signale ausgeben.

## Installation

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e .[dev]
```

## Demo

```powershell
pv-kwp-inference --positions beispiele/invoice_positions.csv --output demo_output/kwp_by_project.csv
```

## Tests

```powershell
python -m pytest
python -m compileall src tests
```

## Datenschutz

Die Beispielpositionen und Projekt-IDs sind synthetisch. Produktive Dokumente,
Projektlisten, Kundeninformationen und lokale API-Anbindungen sind nicht
enthalten.
