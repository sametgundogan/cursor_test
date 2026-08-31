"""Smoke test: every registered SAP chart builds a Plotly figure."""

from sap_gallery.charts import CHARTS


def test_every_chart_builds():
    assert len(CHARTS) >= 40
    ids = [c["id"] for c in CHARTS]
    assert len(ids) == len(set(ids))
    for spec in CHARTS:
        fig = spec["build"]()
        assert fig.data, spec["id"]
        assert fig.to_json()


if __name__ == "__main__":
    test_every_chart_builds()
    print(f"ok: {len(CHARTS)} charts")
