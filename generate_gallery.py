#!/usr/bin/env python3
"""Build a standalone SAP Plotly chart gallery (gallery/index.html)."""

from __future__ import annotations

import json
from pathlib import Path

from sap_gallery.charts import CHARTS

ROOT = Path(__file__).resolve().parent
OUT_DIR = ROOT / "gallery"
TEMPLATE = ROOT / "sap_gallery" / "index.template.html"


def build_catalog() -> list[dict]:
    catalog = []
    for spec in CHARTS:
        fig = spec["build"]()
        payload = json.loads(fig.to_json())
        catalog.append(
            {
                "id": spec["id"],
                "title": spec["title"],
                "plotly_type": spec["plotly_type"],
                "module": spec["module"],
                "objects": spec["objects"],
                "use_case": spec["use_case"],
                "wide": spec["wide"],
                "height": spec["height"],
                "figure": payload,
            }
        )
    return catalog


def main() -> None:
    OUT_DIR.mkdir(exist_ok=True)
    catalog = build_catalog()
    html = TEMPLATE.read_text(encoding="utf-8")
    html = html.replace("/*__CATALOG__*/", json.dumps(catalog, ensure_ascii=False))
    html = html.replace("__COUNT__", str(len(catalog)))
    (OUT_DIR / "index.html").write_text(html, encoding="utf-8")
    print(f"Wrote {OUT_DIR / 'index.html'} with {len(catalog)} charts")


if __name__ == "__main__":
    main()
