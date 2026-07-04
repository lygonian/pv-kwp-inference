"""CLI for synthetic PV kWp inference."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from .kwp import infer_project_kwp


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Infer synthetic PV kWp per project.")
    parser.add_argument("--positions", default="beispiele/invoice_positions.csv")
    parser.add_argument("--output", default="demo_output/kwp_by_project.csv")
    args = parser.parse_args(argv)

    result = infer_project_kwp(pd.read_csv(args.positions))
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(output, index=False, encoding="utf-8-sig")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
