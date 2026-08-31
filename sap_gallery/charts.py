"""SAP/ERP sample charts — one short example per Plotly type."""

from __future__ import annotations

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from sap_gallery.theme import SAP_COLORS, style

CHARTS: list[dict] = []


def register(
    *,
    id: str,
    title: str,
    plotly_type: str,
    module: str,
    objects: str,
    use_case: str,
    wide: bool = False,
    height: int = 380,
):
    def deco(fn):
        CHARTS.append(
            {
                "id": id,
                "title": title,
                "plotly_type": plotly_type,
                "module": module,
                "objects": objects,
                "use_case": use_case,
                "wide": wide,
                "height": height,
                "build": fn,
            }
        )
        return fn

    return deco


# ---------------------------------------------------------------------------
# Bars / columns
# ---------------------------------------------------------------------------


@register(
    id="bar",
    title="Satış organizasyonuna göre net ciro",
    plotly_type="Bar",
    module="SD",
    objects="VBAK, VBAK-VKORG, VBAK-NETWR",
    use_case="Satış organizasyonu (VKORG) bazında dönem cirosu.",
)
def chart_bar():
    df = pd.DataFrame(
        {
            "vkorg": ["1000 DE", "2000 TR", "3000 US", "4000 FR", "5000 NL"],
            "netwr": [12.4, 8.1, 6.7, 4.2, 3.5],
        }
    )
    fig = px.bar(df, x="vkorg", y="netwr", text="netwr", color="vkorg")
    fig.update_traces(texttemplate="%{text:.1f} M€", textposition="outside", showlegend=False)
    fig.update_layout(yaxis_title="Net ciro (M€)", xaxis_title="Satış organizasyonu")
    return style(fig)


@register(
    id="grouped-bar",
    title="Maliyet merkezi: fiili vs bütçe",
    plotly_type="Grouped bar",
    module="CO",
    objects="COSP, COSS, CSKS",
    use_case="Fiili giderin bütçeye göre sapması (plan/actual).",
)
def chart_grouped_bar():
    df = pd.DataFrame(
        {
            "kostl": ["Production", "Quality", "Logistics", "Admin"] * 2,
            "tur": ["Fiili"] * 4 + ["Bütçe"] * 4,
            "tutar": [1.82, 0.64, 0.91, 0.47, 1.70, 0.70, 0.85, 0.50],
        }
    )
    fig = px.bar(df, x="kostl", y="tutar", color="tur", barmode="group")
    fig.update_layout(yaxis_title="Gider (M€)", xaxis_title="Maliyet merkezi")
    return style(fig)


@register(
    id="stacked-bar",
    title="Dağıtım kanalına göre ciro kırılımı",
    plotly_type="Stacked bar",
    module="SD",
    objects="VBAK-VTWEG, VBAK-NETWR",
    use_case="Direkt, bayi ve e-ticaret kanallarının aylık payı.",
)
def chart_stacked_bar():
    months = ["Oca", "Şub", "Mar", "Nis", "May", "Haz"]
    df = pd.DataFrame(
        {
            "ay": months * 3,
            "kanal": ["10 Direkt"] * 6 + ["20 Bayi"] * 6 + ["30 E-ticaret"] * 6,
            "ciro": [2.1, 2.0, 2.4, 2.3, 2.6, 2.5, 1.4, 1.5, 1.6, 1.5, 1.7, 1.8, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1],
        }
    )
    fig = px.bar(df, x="ay", y="ciro", color="kanal", barmode="stack")
    fig.update_layout(yaxis_title="Ciro (M€)", xaxis_title="Ay")
    return style(fig)


@register(
    id="horizontal-bar",
    title="En yüksek harcama yapılan tedarikçiler",
    plotly_type="Horizontal bar",
    module="MM",
    objects="EKKO, EKPO, LFA1",
    use_case="Satınalma siparişi tutarına göre top tedarikçi (ME2L).",
)
def chart_horizontal_bar():
    df = pd.DataFrame(
        {
            "lifnr": ["Bosch", "Siemens", "Arcelik", "Schneider", "SKF"],
            "harcama": [3.40, 2.85, 2.10, 1.65, 1.20],
        }
    ).sort_values("harcama")
    fig = px.bar(df, x="harcama", y="lifnr", orientation="h", text="harcama", color="harcama")
    fig.update_traces(texttemplate="%{text:.2f} M€", textposition="outside", showlegend=False)
    fig.update_layout(xaxis_title="Harcama (M€)", yaxis_title="Tedarikçi", coloraxis_showscale=False)
    return style(fig)


# ---------------------------------------------------------------------------
# Lines / areas
# ---------------------------------------------------------------------------


@register(
    id="line",
    title="Aylık sipariş girişi",
    plotly_type="Line",
    module="SD",
    objects="VBAK-ERDAT, VBAK-NETWR",
    use_case="Incoming orders trendi (VA05 / SIS).",
)
def chart_line():
    df = pd.DataFrame(
        {
            "ay": ["Oca", "Şub", "Mar", "Nis", "May", "Haz", "Tem", "Ağu"],
            "siparis": [4.2, 3.9, 4.8, 4.5, 5.1, 5.4, 4.9, 5.6],
        }
    )
    fig = px.line(df, x="ay", y="siparis", markers=True)
    fig.update_traces(line=dict(width=3))
    fig.update_layout(yaxis_title="Sipariş (M€)", xaxis_title="Ay")
    return style(fig)


@register(
    id="multi-line",
    title="Üretim planı vs fiili",
    plotly_type="Multi-line",
    module="PP",
    objects="PLA, AFKO, AFPO",
    use_case="SOP/MPS planı ile teyit edilen üretim miktarı.",
)
def chart_multi_line():
    df = pd.DataFrame(
        {
            "hafta": [f"W{i:02d}" for i in range(1, 9)] * 2,
            "seri": ["Plan"] * 8 + ["Fiili"] * 8,
            "miktar": [1200, 1250, 1300, 1280, 1350, 1400, 1380, 1420, 1180, 1210, 1290, 1240, 1360, 1370, 1410, 1390],
        }
    )
    fig = px.line(df, x="hafta", y="miktar", color="seri", markers=True)
    fig.update_layout(yaxis_title="Adet", xaxis_title="Hafta")
    return style(fig)


@register(
    id="area",
    title="Stok değeri trendi",
    plotly_type="Area",
    module="MM",
    objects="MBEW, MARD",
    use_case="Tesis stok değerinin zamana göre seyri (MC.9).",
)
def chart_area():
    df = pd.DataFrame(
        {
            "ay": ["Oca", "Şub", "Mar", "Nis", "May", "Haz"],
            "stok": [18.2, 17.6, 19.1, 18.4, 17.9, 16.8],
        }
    )
    fig = px.area(df, x="ay", y="stok")
    fig.update_layout(yaxis_title="Stok değeri (M€)", xaxis_title="Ay")
    return style(fig)


@register(
    id="stacked-area",
    title="Gider unsuru kırılımı",
    plotly_type="Stacked area",
    module="CO",
    objects="COSP, KSTAR",
    use_case="Personel, malzeme, enerji ve dış hizmet giderleri.",
)
def chart_stacked_area():
    months = ["Oca", "Şub", "Mar", "Nis", "May", "Haz"]
    df = pd.DataFrame(
        {
            "ay": months * 4,
            "unsur": ["Personel"] * 6 + ["Malzeme"] * 6 + ["Enerji"] * 6 + ["Hizmet"] * 6,
            "tutar": (
                [1.1, 1.1, 1.2, 1.2, 1.3, 1.3]
                + [0.8, 0.9, 0.85, 0.95, 1.0, 0.9]
                + [0.3, 0.28, 0.32, 0.3, 0.35, 0.4]
                + [0.2, 0.22, 0.21, 0.25, 0.24, 0.26]
            ),
        }
    )
    fig = px.area(df, x="ay", y="tutar", color="unsur")
    fig.update_layout(yaxis_title="Gider (M€)", xaxis_title="Ay")
    return style(fig)


@register(
    id="range-area",
    title="Min–max stok bandı ve fiili stok",
    plotly_type="Range area",
    module="MM",
    objects="MARC-EISBE, MARC-MABST, MARD-LABST",
    use_case="Güvenlik stoğu ile maksimum stok arasındaki fiili seviye.",
)
def chart_range_area():
    weeks = [f"W{i:02d}" for i in range(1, 9)]
    lo, hi, actual = [80] * 8, [160] * 8, [95, 110, 140, 150, 125, 100, 90, 118]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=weeks + weeks[::-1], y=hi + lo[::-1], fill="toself", fillcolor="rgba(0,112,242,0.12)", line=dict(width=0), name="Min–max bandı", hoverinfo="skip"))
    fig.add_trace(go.Scatter(x=weeks, y=actual, mode="lines+markers", name="Fiili stok", line=dict(color="#0070F2", width=3)))
    fig.update_layout(yaxis_title="Adet", xaxis_title="Hafta")
    return style(fig)


@register(
    id="error-bars",
    title="Talep tahmini ve sapma bandı",
    plotly_type="Error bars",
    module="PP",
    objects="PBED, PBIM",
    use_case="SOP tahmininin ± sapma aralığı.",
)
def chart_error_bars():
    df = pd.DataFrame(
        {
            "ay": ["Oca", "Şub", "Mar", "Nis", "May", "Haz"],
            "tahmin": [820, 840, 900, 880, 950, 980],
            "sapma": [40, 35, 50, 45, 55, 60],
        }
    )
    fig = go.Figure(
        go.Scatter(
            x=df["ay"],
            y=df["tahmin"],
            error_y=dict(type="data", array=df["sapma"], visible=True, color="#E76500"),
            mode="lines+markers",
            name="Tahmin",
        )
    )
    fig.update_layout(yaxis_title="Adet", xaxis_title="Ay")
    return style(fig)


# ---------------------------------------------------------------------------
# Scatter family
# ---------------------------------------------------------------------------


@register(
    id="scatter",
    title="Teslimat süresi vs mesafe",
    plotly_type="Scatter",
    module="LE",
    objects="LIKP, VTTK",
    use_case="Sevkiyat mesafesine göre fiili teslim günü.",
)
def chart_scatter():
    rng = np.random.default_rng(7)
    km = rng.uniform(40, 900, 40)
    gun = 0.8 + km / 420 + rng.normal(0, 0.35, 40)
    df = pd.DataFrame({"km": km, "gun": gun.clip(0.5, 5)})
    fig = px.scatter(df, x="km", y="gun")
    fig.update_layout(xaxis_title="Mesafe (km)", yaxis_title="Teslimat (gün)")
    return style(fig)


@register(
    id="bubble",
    title="Müşteri portföyü: ciro, marj, hacim",
    plotly_type="Bubble",
    module="SD",
    objects="KNA1, VBAK, VBAP, KOMP",
    use_case="Müşteri bazında ciro (x), marj (y), sipariş hacmi (balon).",
)
def chart_bubble():
    df = pd.DataFrame(
        {
            "musteri": ["A101", "A205", "B010", "C330", "D018", "E440"],
            "ciro": [2.4, 1.8, 3.1, 0.9, 1.2, 2.0],
            "marj": [18, 22, 12, 28, 15, 20],
            "hacim": [420, 210, 610, 90, 150, 300],
        }
    )
    fig = px.scatter(df, x="ciro", y="marj", size="hacim", color="musteri", hover_name="musteri", size_max=48)
    fig.update_layout(xaxis_title="Ciro (M€)", yaxis_title="Marj (%)")
    return style(fig)


@register(
    id="splom",
    title="Finansal oranlar matrisi",
    plotly_type="Scatter matrix (SPLOM)",
    module="FI",
    objects="FAGLFLEXT, SKB1",
    use_case="Likidite, kârlılık ve çevrim oranlarının birbirine bakışı.",
    wide=True,
    height=520,
)
def chart_splom():
    rng = np.random.default_rng(3)
    df = pd.DataFrame(
        {
            "DSO": rng.normal(42, 8, 24).clip(20, 70),
            "DPO": rng.normal(35, 7, 24).clip(15, 55),
            "Stok gün": rng.normal(55, 10, 24).clip(25, 80),
            "Brüt marj": rng.normal(24, 4, 24).clip(12, 36),
        }
    )
    fig = px.scatter_matrix(df)
    fig.update_traces(diagonal_visible=False, showupperhalf=False)
    return style(fig, height=520)


# ---------------------------------------------------------------------------
# Parts of a whole
# ---------------------------------------------------------------------------


@register(
    id="pie",
    title="Satış bölümü ciro payı",
    plotly_type="Pie",
    module="SD",
    objects="VBAK-SPART",
    use_case="Division (SPART) bazında ciro dağılımı.",
)
def chart_pie():
    df = pd.DataFrame({"spart": ["01 Beyaz eşya", "02 TV", "03 Klima", "04 Yedek parça"], "ciro": [44, 28, 18, 10]})
    fig = px.pie(df, names="spart", values="ciro")
    fig.update_traces(textinfo="percent+label")
    return style(fig, axes=False)


@register(
    id="donut",
    title="Stok ABC sınıfı",
    plotly_type="Donut",
    module="MM",
    objects="MBEW, MARC",
    use_case="ABC analizi: stok değerinin sınıf dağılımı.",
)
def chart_donut():
    df = pd.DataFrame({"sinif": ["A", "B", "C"], "deger": [72, 19, 9]})
    fig = px.pie(df, names="sinif", values="deger", hole=0.55)
    fig.update_traces(textinfo="percent+label")
    fig.add_annotation(text="ABC", x=0.5, y=0.5, showarrow=False, font=dict(size=18, color="#1D2D3E"))
    return style(fig, axes=False)


@register(
    id="sunburst",
    title="Kâr merkezi hiyerarşisinde gider",
    plotly_type="Sunburst",
    module="CO",
    objects="CEPC, CSKS, COSP",
    use_case="Şirket kodu → kâr merkezi → gider türü kırılımı.",
    wide=True,
)
def chart_sunburst():
    df = pd.DataFrame(
        {
            "sirket": ["1000"] * 6,
            "prctr": ["P100 Üretim", "P100 Üretim", "P200 Satış", "P200 Satış", "P300 Lojistik", "P300 Lojistik"],
            "kstar": ["Personel", "Malzeme", "Personel", "Pazarlama", "Personel", "Nakliye"],
            "tutar": [2.1, 3.4, 0.9, 0.6, 0.5, 0.8],
        }
    )
    fig = px.sunburst(df, path=["sirket", "prctr", "kstar"], values="tutar")
    return style(fig, axes=False)


@register(
    id="treemap",
    title="Tesis ve malzeme grubuna göre stok değeri",
    plotly_type="Treemap",
    module="MM",
    objects="MARD, MARA-MATKL, T001W",
    use_case="Stok değerinin tesis × malzeme grubu hiyerarşisi.",
    wide=True,
)
def chart_treemap():
    df = pd.DataFrame(
        {
            "tesis": ["1010"] * 3 + ["2010"] * 3,
            "matkl": ["Elektronik", "Mekanik", "Ambalaj"] * 2,
            "deger": [4.8, 2.1, 0.6, 3.2, 1.7, 0.4],
        }
    )
    fig = px.treemap(df, path=["tesis", "matkl"], values="deger")
    return style(fig, axes=False)


@register(
    id="icicle",
    title="Bilanço hesap hiyerarşisi",
    plotly_type="Icicle",
    module="FI",
    objects="SKA1, FAGLFLEXT",
    use_case="Varlıklar altında nakit, alacak ve stok bakiyeleri.",
    wide=True,
)
def chart_icicle():
    df = pd.DataFrame(
        {
            "sinif": ["Varlıklar"] * 5,
            "grup": ["Dönen"] * 3 + ["Duran"] * 2,
            "hesap": ["Kasa/Banka", "Alacaklar", "Stoklar", "Maddi duran", "Maddi olmayan"],
            "bakiye": [4.2, 6.8, 16.5, 22.0, 3.1],
        }
    )
    fig = px.icicle(df, path=["sinif", "grup", "hesap"], values="bakiye")
    return style(fig, axes=False)


@register(
    id="funnel",
    title="Order-to-Cash hunisi",
    plotly_type="Funnel",
    module="SD",
    objects="VA21, VBAK, LIKP, VBRK, BSID",
    use_case="Teklif → sipariş → teslimat → fatura → tahsilat.",
)
def chart_funnel():
    fig = go.Figure(
        go.Funnel(
            y=["Teklif", "Sipariş", "Teslimat", "Fatura", "Tahsilat"],
            x=[100, 74, 68, 65, 58],
            textinfo="value+percent initial",
        )
    )
    fig.update_layout(xaxis_title="Değer (indeks 100 = teklif)")
    return style(fig, axes=False)


@register(
    id="funnelarea",
    title="Procure-to-Pay hunisi",
    plotly_type="Funnelarea",
    module="MM",
    objects="EBAN, EKKO, MKPF, RBKP",
    use_case="Satınalma talebi → SAS → mal giriş → fatura.",
)
def chart_funnelarea():
    fig = go.Figure(
        go.Funnelarea(
            labels=["Satınalma talebi", "SAS", "Mal giriş", "Fatura (MIRO)"],
            values=[120, 95, 88, 84],
        )
    )
    return style(fig, axes=False)


@register(
    id="waterfall",
    title="Gelir tablosu köprüsü",
    plotly_type="Waterfall",
    module="FI",
    objects="FAGLFLEXT, P&L hesapları",
    use_case="Cirodan net kâra köprü (FI gelir tablosu).",
    wide=True,
)
def chart_waterfall():
    fig = go.Figure(
        go.Waterfall(
            x=["Ciro", "COGS", "Brüt kâr", "OpEx", "FVÖK", "Faiz/vergi", "Net kâr"],
            y=[24.0, -14.5, None, -6.2, None, -1.1, None],
            measure=["relative", "relative", "total", "relative", "total", "relative", "total"],
            connector={"line": {"color": "#D9D9D9"}},
        )
    )
    fig.update_layout(yaxis_title="M€")
    return style(fig)


@register(
    id="waffle",
    title="Stok durumu (100 birim)",
    plotly_type="Waffle",
    module="MM",
    objects="MARD-LABST, MARD-SPEME, MARD-INSME",
    use_case="Kullanılabilir, kalite ve bloke stoğun 100 karelik özeti.",
)
def chart_waffle():
    # 72 unrestricted, 18 QI, 10 blocked
    status = ["Kullanılabilir"] * 72 + ["Kalite"] * 18 + ["Bloke"] * 10
    grid = np.array(status).reshape(10, 10)
    color_map = {"Kullanılabilir": 0, "Kalite": 1, "Bloke": 2}
    z = np.vectorize(color_map.get)(grid)
    fig = go.Figure(
        go.Heatmap(
            z=z,
            colorscale=[[0, "#256F3A"], [0.5, "#E76500"], [1, "#AA0808"]],
            showscale=False,
            hovertemplate="%{text}<extra></extra>",
            text=grid,
            xgap=3,
            ygap=3,
        )
    )
    fig.update_xaxes(visible=False)
    fig.update_yaxes(visible=False, autorange="reversed")
    fig.update_layout(
        annotations=[
            dict(x=1.02, y=0.7, xref="paper", text="Kullanılabilir 72%", showarrow=False, xanchor="left"),
            dict(x=1.02, y=0.5, xref="paper", text="Kalite 18%", showarrow=False, xanchor="left"),
            dict(x=1.02, y=0.3, xref="paper", text="Bloke 10%", showarrow=False, xanchor="left"),
        ],
        margin=dict(r=160),
    )
    return style(fig, axes=False)


@register(
    id="marimekko",
    title="Ürün × bölge kâr katkısı",
    plotly_type="Marimekko / mosaic",
    module="CO-PA",
    objects="CE1xxxx, ARTNR, KNDNR",
    use_case="Genişlik = ciro payı, yükseklik = segment payı (CO-PA).",
    wide=True,
)
def chart_marimekko():
    # widths = product revenue share; stacks = region
    products = ["Beyaz eşya", "TV", "Klima"]
    widths = np.array([0.48, 0.32, 0.20])
    lefts = np.cumsum(np.concatenate([[0], widths[:-1]]))
    centers = lefts + widths / 2
    regions = ["TR", "DE", "US"]
    shares = {
        "TR": [0.55, 0.30, 0.40],
        "DE": [0.30, 0.45, 0.35],
        "US": [0.15, 0.25, 0.25],
    }
    fig = go.Figure()
    colors = {"TR": "#0070F2", "DE": "#E76500", "US": "#256F3A"}
    for region in regions:
        fig.add_trace(
            go.Bar(
                x=lefts,
                y=shares[region],
                width=widths,
                name=region,
                marker_color=colors[region],
                offset=0,
            )
        )
    fig.update_layout(
        barmode="stack",
        xaxis=dict(tickmode="array", tickvals=list(centers), ticktext=products, range=[0, 1]),
        yaxis_title="Pay",
        xaxis_title="Ürün (genişlik = ciro payı)",
    )
    return style(fig)


# ---------------------------------------------------------------------------
# KPIs
# ---------------------------------------------------------------------------


@register(
    id="indicator",
    title="DSO (alacak tahsil süresi)",
    plotly_type="Indicator",
    module="FI",
    objects="BSID, KNA1",
    use_case="Days Sales Outstanding; hedefle delta.",
    height=260,
)
def chart_indicator():
    fig = go.Figure(
        go.Indicator(
            mode="number+delta",
            value=41.2,
            number={"suffix": " gün", "font": {"size": 48, "color": "#0070F2"}},
            delta={"reference": 45, "decreasing": {"color": "#256F3A"}, "increasing": {"color": "#AA0808"}},
            title={"text": "DSO  ·  hedef 45 gün"},
        )
    )
    return style(fig, height=260, axes=False)


@register(
    id="gauge",
    title="OEE (ekipman etkinliği)",
    plotly_type="Gauge",
    module="PP",
    objects="PP-IS, AFRU, CRHD",
    use_case="Overall Equipment Effectiveness göstergesi.",
    height=300,
)
def chart_gauge():
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=78,
            number={"suffix": "%"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "#0070F2"},
                "steps": [
                    {"range": [0, 60], "color": "#F5D5D5"},
                    {"range": [60, 80], "color": "#FBE3C8"},
                    {"range": [80, 100], "color": "#C8E4D0"},
                ],
                "threshold": {"line": {"color": "#AA0808", "width": 3}, "value": 85},
            },
            title={"text": "OEE"},
        )
    )
    return style(fig, height=300, axes=False)


@register(
    id="bullet",
    title="Stok devir hızı vs hedef",
    plotly_type="Bullet",
    module="MM",
    objects="MBEW, MSEG",
    use_case="Inventory turnover; fiili, hedef ve aralıklar.",
    height=220,
)
def chart_bullet():
    fig = go.Figure(
        go.Indicator(
            mode="number+gauge+delta",
            value=6.4,
            delta={"reference": 7.0},
            gauge={
                "shape": "bullet",
                "axis": {"range": [0, 12]},
                "bar": {"color": "#0070F2"},
                "steps": [
                    {"range": [0, 4], "color": "#F5D5D5"},
                    {"range": [4, 7], "color": "#FBE3C8"},
                    {"range": [7, 12], "color": "#C8E4D0"},
                ],
                "threshold": {"line": {"color": "#1D2D3E", "width": 3}, "value": 7.0},
            },
            title={"text": "Devir / yıl"},
        )
    )
    fig.update_layout(margin=dict(t=60, b=40))
    return style(fig, height=220, axes=False)


# ---------------------------------------------------------------------------
# Heatmaps / 2D density
# ---------------------------------------------------------------------------


@register(
    id="heatmap",
    title="İş yeri × hafta kapasite kullanımı",
    plotly_type="Heatmap",
    module="PP",
    objects="CRHD, KAKO, KBED",
    use_case="Work center yükü (%); kırmızı = aşırı yük.",
)
def chart_heatmap():
    wcs = ["WC-Pres", "WC-Montaj", "WC-Boya", "WC-Test"]
    weeks = [f"W{i:02d}" for i in range(1, 7)]
    z = [
        [72, 81, 95, 88, 76, 70],
        [64, 70, 77, 92, 85, 80],
        [55, 60, 68, 74, 90, 96],
        [40, 45, 52, 58, 61, 66],
    ]
    fig = go.Figure(go.Heatmap(z=z, x=weeks, y=wcs, colorscale="Blues", colorbar=dict(title="%")))
    fig.update_layout(xaxis_title="Hafta", yaxis_title="İş yeri")
    return style(fig, axes=False)


@register(
    id="annotated-heatmap",
    title="Tesis × hata türü adedi",
    plotly_type="Annotated heatmap",
    module="QM",
    objects="QMEL, QMUR, QPCT",
    use_case="Kalite bildirimi (Q1) adetleri.",
)
def chart_annotated_heatmap():
    plants = ["1010", "2010", "3010"]
    defects = ["Çizik", "Ölçü", "Paket", "Fonksiyon"]
    z = [[12, 4, 7, 2], [5, 15, 3, 6], [2, 3, 9, 11]]
    fig = go.Figure(
        go.Heatmap(
            z=z,
            x=defects,
            y=plants,
            colorscale="YlOrRd",
            text=z,
            texttemplate="%{text}",
            hovertemplate="Tesis %{y}<br>%{x}: %{z}<extra></extra>",
        )
    )
    fig.update_layout(xaxis_title="Hata türü", yaxis_title="Tesis")
    return style(fig, axes=False)


@register(
    id="calendar-heatmap",
    title="FI belge kayıt adedi (takvim)",
    plotly_type="Calendar heatmap",
    module="FI",
    objects="BKPF-BUDAT",
    use_case="Günlük muhasebe belge yoğunluğu.",
    wide=True,
)
def chart_calendar_heatmap():
    rng = np.random.default_rng(11)
    days = pd.date_range("2026-03-01", "2026-03-31", freq="D")
    # weekdays busier
    counts = []
    for d in days:
        base = 18 if d.weekday() < 5 else 3
        counts.append(int(rng.integers(base, base + 25)))
    df = pd.DataFrame({"tarih": days, "adet": counts})
    df["hafta"] = df["tarih"].dt.isocalendar().week.astype(int)
    df["gun"] = df["tarih"].dt.weekday
    gun_ad = ["Pzt", "Sal", "Çar", "Per", "Cum", "Cmt", "Paz"]
    pivot = df.pivot_table(index="hafta", columns="gun", values="adet")
    fig = go.Figure(
        go.Heatmap(
            z=pivot.values,
            x=[gun_ad[c] for c in pivot.columns],
            y=[f"W{int(w):02d}" for w in pivot.index],
            colorscale="Blues",
            colorbar=dict(title="Belge"),
        )
    )
    fig.update_layout(xaxis_title="Gün", yaxis_title="Hafta")
    return style(fig, axes=False)


@register(
    id="density-heatmap",
    title="Sipariş saati × haftanın günü",
    plotly_type="Density heatmap",
    module="SD",
    objects="VBAK-ERDAT, VBAK-ERZET",
    use_case="Sipariş yaratma yoğunluğu (müşteri hizmetleri kapasitesi).",
)
def chart_density_heatmap():
    rng = np.random.default_rng(5)
    weekday = rng.integers(0, 5, 400)
    hour = rng.normal(11, 3, 400).clip(8, 18)
    df = pd.DataFrame({"gun": weekday, "saat": hour})
    fig = px.density_heatmap(df, x="gun", y="saat", nbinsx=5, nbinsy=10)
    fig.update_xaxes(tickmode="array", tickvals=list(range(5)), ticktext=["Pzt", "Sal", "Çar", "Per", "Cum"])
    fig.update_layout(xaxis_title="Gün", yaxis_title="Saat")
    return style(fig, axes=False)


@register(
    id="density-contour",
    title="Fiyat × miktar yoğunluğu",
    plotly_type="Density contour",
    module="SD",
    objects="VBAP-NETPR, VBAP-KWMENG",
    use_case="Sipariş kalemlerinin fiyat-miktar kümelenmesi.",
)
def chart_density_contour():
    rng = np.random.default_rng(2)
    df = pd.DataFrame(
        {
            "fiyat": rng.lognormal(3.2, 0.35, 250),
            "miktar": rng.lognormal(4.0, 0.5, 250),
        }
    )
    fig = px.density_contour(df, x="fiyat", y="miktar")
    fig.update_traces(contours_coloring="fill", colorbar=dict(title="Yoğunluk"))
    fig.update_layout(xaxis_title="Net fiyat (€)", yaxis_title="Miktar")
    return style(fig)


@register(
    id="contour",
    title="Parti × hacme göre birim maliyet",
    plotly_type="Contour",
    module="CO",
    objects="CK11N, KEKO, KEPH",
    use_case="Parti büyüklüğü ve yıllık hacme göre standart maliyet.",
)
def chart_contour():
    lot = np.linspace(50, 500, 20)
    vol = np.linspace(1, 20, 20)
    L, V = np.meshgrid(lot, vol)
    cost = 42 + 800 / L + 15 / V
    fig = go.Figure(go.Contour(x=lot, y=vol, z=cost, colorscale="Teal", colorbar=dict(title="€/adet")))
    fig.update_layout(xaxis_title="Parti büyüklüğü", yaxis_title="Yıllık hacim (bin adet)")
    return style(fig, axes=False)


@register(
    id="histogram2d",
    title="Sipariş tutarı × teslimat gecikmesi",
    plotly_type="Histogram2d",
    module="SD",
    objects="VBAK, LIKP, VBEP-EDATU",
    use_case="Değer ile gecikme gününün ortak dağılımı.",
)
def chart_histogram2d():
    rng = np.random.default_rng(9)
    df = pd.DataFrame(
        {
            "tutar": rng.lognormal(8.5, 0.6, 300),
            "gecikme": rng.normal(1.5, 2.2, 300).clip(-2, 12),
        }
    )
    fig = go.Figure(go.Histogram2d(x=df["tutar"], y=df["gecikme"], colorscale="Blues"))
    fig.update_layout(xaxis_title="Sipariş tutarı (€)", yaxis_title="Gecikme (gün)")
    return style(fig, axes=False)


@register(
    id="imshow",
    title="KPI korelasyon matrisi",
    plotly_type="Imshow",
    module="FI",
    objects="KPI seti (DSO, DPO, stok, marj, OTD)",
    use_case="Çalışma sermayesi ve teslimat KPI’larının korelasyonu.",
)
def chart_imshow():
    labels = ["DSO", "DPO", "Stok gün", "Marj", "OTD"]
    z = [
        [1.00, -0.22, 0.31, -0.18, -0.40],
        [-0.22, 1.00, -0.10, 0.05, 0.12],
        [0.31, -0.10, 1.00, -0.28, -0.15],
        [-0.18, 0.05, -0.28, 1.00, 0.35],
        [-0.40, 0.12, -0.15, 0.35, 1.00],
    ]
    fig = px.imshow(z, x=labels, y=labels, color_continuous_scale="RdBu", zmin=-1, zmax=1, text_auto=True)
    return style(fig, axes=False)


@register(
    id="cohort",
    title="Müşteri tekrar sipariş kohortu",
    plotly_type="Cohort heatmap",
    module="SD",
    objects="VBAK-KUNNR, VBAK-ERDAT",
    use_case="İlk sipariş ayına göre sonraki aylarda tekrar alım oranı.",
)
def chart_cohort():
    z = [
        [100, 42, 31, 24, 20],
        [100, 45, 33, 22, None],
        [100, 38, 28, None, None],
        [100, 41, None, None, None],
        [100, None, None, None, None],
    ]
    fig = go.Figure(
        go.Heatmap(
            z=z,
            x=["Ay 0", "Ay 1", "Ay 2", "Ay 3", "Ay 4"],
            y=["Oca kohort", "Şub kohort", "Mar kohort", "Nis kohort", "May kohort"],
            colorscale="Blues",
            text=z,
            texttemplate="%{text}",
        )
    )
    fig.update_layout(xaxis_title="Kohort yaşı", yaxis_title="İlk sipariş ayı")
    return style(fig, axes=False)


# ---------------------------------------------------------------------------
# Distributions
# ---------------------------------------------------------------------------


@register(
    id="histogram",
    title="Fatura tutarı dağılımı",
    plotly_type="Histogram",
    module="FI",
    objects="BSEG, VBRK-NETWR",
    use_case="Satış faturalarının tutar histogramı.",
)
def chart_histogram():
    rng = np.random.default_rng(4)
    df = pd.DataFrame({"tutar": rng.lognormal(7.8, 0.55, 400)})
    fig = px.histogram(df, x="tutar", nbins=24)
    fig.update_layout(xaxis_title="Fatura tutarı (€)", yaxis_title="Adet")
    return style(fig)


@register(
    id="box",
    title="Tedarikçi teslim süresi",
    plotly_type="Box",
    module="MM",
    objects="EKET-EINDT, EKET-SLFDT, LFA1",
    use_case="Planlanan vs fiili teslim günü dağılımı (vendor evaluation).",
)
def chart_box():
    rng = np.random.default_rng(6)
    rows = []
    for name, mu in [("Bosch", 8), ("Siemens", 11), ("SKF", 14)]:
        for v in rng.normal(mu, 2.2, 28):
            rows.append({"tedarikci": name, "gun": max(2, v)})
    fig = px.box(pd.DataFrame(rows), x="tedarikci", y="gun", color="tedarikci")
    fig.update_layout(yaxis_title="Teslim süresi (gün)", xaxis_title="Tedarikçi", showlegend=False)
    return style(fig)


@register(
    id="violin",
    title="Üretim emri çevrim süresi",
    plotly_type="Violin",
    module="PP",
    objects="AFKO-GSTRP, AFKO-GETRI",
    use_case="İş emri açılış–kapanış günlerinin dağılımı.",
)
def chart_violin():
    rng = np.random.default_rng(8)
    rows = []
    for tes, mu in [("1010", 6), ("2010", 9)]:
        for v in rng.normal(mu, 1.8, 40):
            rows.append({"tesis": tes, "gun": max(1, v)})
    fig = px.violin(pd.DataFrame(rows), x="tesis", y="gun", color="tesis", box=True, points="outliers")
    fig.update_layout(yaxis_title="Çevrim (gün)", xaxis_title="Tesis", showlegend=False)
    return style(fig)


@register(
    id="strip",
    title="Muayene karakteristik sonuçları",
    plotly_type="Strip",
    module="QM",
    objects="QAMR, QAMV",
    use_case="Ölçüm sonuçlarının spesifikasyon etrafındaki saçılımı.",
)
def chart_strip():
    rng = np.random.default_rng(1)
    df = pd.DataFrame(
        {
            "tesis": np.repeat(["1010", "2010", "3010"], 18),
            "olcum": np.concatenate(
                [rng.normal(50.0, 0.4, 18), rng.normal(50.2, 0.6, 18), rng.normal(49.7, 0.5, 18)]
            ),
        }
    )
    fig = px.strip(df, x="tesis", y="olcum", color="tesis")
    fig.add_hline(y=50, line_dash="dash", line_color="#1D2D3E", annotation_text="Hedef")
    fig.update_layout(yaxis_title="Ölçüm", xaxis_title="Tesis", showlegend=False)
    return style(fig)


@register(
    id="ecdf",
    title="Tedarikçi ödeme günü (ECDF)",
    plotly_type="ECDF",
    module="FI",
    objects="BSIK, LFA1, ZTERM",
    use_case="AP ödemelerinin kaç günde kapandığının kümülatif dağılımı.",
)
def chart_ecdf():
    rng = np.random.default_rng(12)
    df = pd.DataFrame({"gun": rng.normal(32, 9, 200).clip(5, 70)})
    fig = px.ecdf(df, x="gun")
    fig.update_layout(xaxis_title="Ödeme günü", yaxis_title="Kümülatif pay")
    return style(fig)


@register(
    id="ridgeline",
    title="Aylık talep dağılımı",
    plotly_type="Ridgeline",
    module="PP",
    objects="PBED, VBAP",
    use_case="Aylara göre sipariş miktarı yoğunluğu (demand shape).",
    wide=True,
)
def chart_ridgeline():
    months = ["Oca", "Şub", "Mar", "Nis"]
    fig = go.Figure()
    for i, (m, mu) in enumerate(zip(months, [100, 115, 130, 120])):
        xs = np.linspace(40, 200, 80)
        density = np.exp(-0.5 * ((xs - mu) / 18) ** 2)
        density = density / density.max() * 0.85
        base = float(len(months) - i - 1)
        fig.add_trace(
            go.Scatter(
                x=np.concatenate([xs, xs[::-1]]),
                y=np.concatenate([density + base, np.full_like(xs, base)[::-1]]),
                fill="toself",
                name=m,
                mode="lines",
                line=dict(width=1),
            )
        )
    fig.update_layout(xaxis_title="Sipariş miktarı", yaxis_title="Ay (yoğunluk ofseti)")
    return style(fig)


@register(
    id="dendrogram",
    title="Malzeme kümeleme (benzer hareket)",
    plotly_type="Dendrogram",
    module="MM",
    objects="MARA, MSEG",
    use_case="Hareket profiline göre malzeme gruplama (MRP kümesi).",
    wide=True,
    height=420,
)
def chart_dendrogram():
    rng = np.random.default_rng(14)
    labels = ["MAT-A", "MAT-B", "MAT-C", "MAT-D", "MAT-E", "MAT-F", "MAT-G", "MAT-H"]
    data = rng.normal(size=(8, 6))
    data[0:3] += 2
    data[3:5] -= 1.5
    fig = ff.create_dendrogram(data, labels=labels)
    fig.update_layout(xaxis_title="Malzeme", yaxis_title="Uzaklık")
    return style(fig, height=420)


# ---------------------------------------------------------------------------
# Flow / comparison
# ---------------------------------------------------------------------------


@register(
    id="sankey",
    title="Order-to-Cash değer akışı",
    plotly_type="Sankey",
    module="SD",
    objects="VBAK, LIKP, VBRK, BSID",
    use_case="Sipariş değerinin teslimat, fatura ve tahsilata akışı.",
    wide=True,
    height=440,
)
def chart_sankey():
    labels = ["Sipariş", "Teslimat", "Fatura", "Tahsilat", "İptal", "Gecikmiş"]
    fig = go.Figure(
        go.Sankey(
            node=dict(label=labels, pad=16, thickness=14, color=SAP_COLORS[:6]),
            link=dict(
                source=[0, 0, 1, 1, 2, 2],
                target=[1, 4, 2, 4, 3, 5],
                value=[90, 10, 82, 8, 70, 12],
            ),
        )
    )
    return style(fig, height=440, axes=False)


@register(
    id="parcoords",
    title="Tedarikçi karnesi (paralel koordinat)",
    plotly_type="Parallel coordinates",
    module="MM",
    objects="ME61, EINA, EKPO",
    use_case="Fiyat, kalite, teslimat ve servis skorlarının birlikte okunması.",
    wide=True,
)
def chart_parcoords():
    df = pd.DataFrame(
        {
            "fiyat": [80, 70, 90, 60, 75],
            "kalite": [85, 92, 70, 88, 78],
            "teslimat": [90, 75, 65, 95, 80],
            "servis": [70, 88, 60, 85, 72],
            "skor": [82, 81, 71, 82, 76],
        }
    )
    fig = px.parallel_coordinates(df, color="skor", color_continuous_scale="Blues")
    return style(fig, axes=False)


@register(
    id="parcats",
    title="Sipariş durum yolları",
    plotly_type="Parallel categories",
    module="SD",
    objects="VBUK, VBUP",
    use_case="Sipariş türü → teslimat durumu → fatura durumu akışı.",
    wide=True,
)
def chart_parcats():
    df = pd.DataFrame(
        {
            "tur": ["OR"] * 6 + ["RE"] * 3 + ["ZFOC"] * 2,
            "teslimat": ["Tam"] * 5 + ["Kısmi"] * 4 + ["Açık"] * 2,
            "fatura": ["Faturalandı"] * 6 + ["Açık"] * 5,
            "adet": [40, 18, 12, 9, 7, 6, 8, 5, 4, 3, 2],
        }
    )
    fig = px.parallel_categories(df, dimensions=["tur", "teslimat", "fatura"], color="adet")
    return style(fig, axes=False)


@register(
    id="network",
    title="BOM malzeme ağı",
    plotly_type="Network",
    module="MM",
    objects="MAST, STPO, MARA",
    use_case="Üst malzeme ve bileşen ilişkisi (CS03).",
    wide=True,
)
def chart_network():
    nodes = {
        "FG-100": (0, 0),
        "SA-10": (-1, -1),
        "SA-20": (1, -1),
        "RM-A": (-1.6, -2),
        "RM-B": (-0.4, -2),
        "RM-C": (1.0, -2),
        "RM-D": (1.8, -2),
    }
    edges = [("FG-100", "SA-10"), ("FG-100", "SA-20"), ("SA-10", "RM-A"), ("SA-10", "RM-B"), ("SA-20", "RM-C"), ("SA-20", "RM-D")]
    fig = go.Figure()
    for a, b in edges:
        fig.add_trace(
            go.Scatter(
                x=[nodes[a][0], nodes[b][0]],
                y=[nodes[a][1], nodes[b][1]],
                mode="lines",
                line=dict(color="#B8BEC4", width=2),
                hoverinfo="skip",
                showlegend=False,
            )
        )
    fig.add_trace(
        go.Scatter(
            x=[p[0] for p in nodes.values()],
            y=[p[1] for p in nodes.values()],
            mode="markers+text",
            text=list(nodes),
            textposition="top center",
            marker=dict(size=[28, 22, 22, 16, 16, 16, 16], color=["#0070F2", "#E76500", "#E76500", "#256F3A", "#256F3A", "#256F3A", "#256F3A"]),
            showlegend=False,
        )
    )
    fig.update_xaxes(visible=False)
    fig.update_yaxes(visible=False)
    return style(fig, axes=False)


@register(
    id="pareto",
    title="Kalite hataları Pareto",
    plotly_type="Pareto (bar + line)",
    module="QM",
    objects="QMEL, QMUR",
    use_case="Hata türlerinin 80/20 kırılımı.",
)
def chart_pareto():
    df = pd.DataFrame(
        {"hata": ["Çizik", "Ölçü", "Paket", "Fonksiyon", "Etiket", "Diğer"], "adet": [48, 22, 14, 8, 5, 3]}
    )
    df["kum"] = df["adet"].cumsum() / df["adet"].sum() * 100
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Bar(x=df["hata"], y=df["adet"], name="Adet"), secondary_y=False)
    fig.add_trace(go.Scatter(x=df["hata"], y=df["kum"], name="Kümülatif %", mode="lines+markers"), secondary_y=True)
    fig.update_yaxes(title_text="Adet", secondary_y=False)
    fig.update_yaxes(title_text="Kümülatif %", secondary_y=True, range=[0, 100])
    return style(fig)


@register(
    id="combo",
    title="Ciro ve marj %",
    plotly_type="Combo bar + line",
    module="SD",
    objects="VBAK, VBAP, KOMP",
    use_case="Aylık ciro kolon, brüt marj çizgi.",
)
def chart_combo():
    ay = ["Oca", "Şub", "Mar", "Nis", "May", "Haz"]
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Bar(x=ay, y=[4.1, 3.8, 4.6, 4.4, 5.0, 5.2], name="Ciro (M€)"), secondary_y=False)
    fig.add_trace(go.Scatter(x=ay, y=[21, 20, 22, 19, 23, 24], name="Marj %", mode="lines+markers"), secondary_y=True)
    fig.update_yaxes(title_text="Ciro (M€)", secondary_y=False)
    fig.update_yaxes(title_text="Marj %", secondary_y=True)
    return style(fig)


@register(
    id="dumbbell",
    title="Plan vs fiili (maliyet merkezi)",
    plotly_type="Dumbbell",
    module="CO",
    objects="COSP, COSP-WKG00",
    use_case="Bütçe ve fiili arasındaki farkın tek bakışta görülmesi.",
)
def chart_dumbbell():
    df = pd.DataFrame(
        {
            "cc": ["Production", "Quality", "Logistics", "Admin"],
            "plan": [1.70, 0.70, 0.85, 0.50],
            "fiili": [1.82, 0.64, 0.91, 0.47],
        }
    )
    fig = go.Figure()
    for _, r in df.iterrows():
        fig.add_trace(
            go.Scatter(
                x=[r["plan"], r["fiili"]],
                y=[r["cc"], r["cc"]],
                mode="lines",
                line=dict(color="#B8BEC4", width=3),
                showlegend=False,
            )
        )
    fig.add_trace(go.Scatter(x=df["plan"], y=df["cc"], mode="markers", name="Plan", marker=dict(size=12, color="#5D36FF")))
    fig.add_trace(go.Scatter(x=df["fiili"], y=df["cc"], mode="markers", name="Fiili", marker=dict(size=12, color="#0070F2")))
    fig.update_layout(xaxis_title="M€", yaxis_title="Maliyet merkezi")
    return style(fig)


@register(
    id="slope",
    title="Bölge cirosu yıl karşılaştırması",
    plotly_type="Slope",
    module="SD",
    objects="VBAK, KNA1-REGIO",
    use_case="2025 vs 2026 ciro sıralaması / değişimi.",
)
def chart_slope():
    df = pd.DataFrame(
        {
            "bolge": ["Marmara", "Ege", "İç Anadolu", "Akdeniz"],
            "y2025": [5.2, 3.1, 2.4, 1.8],
            "y2026": [5.8, 2.9, 2.8, 2.1],
        }
    )
    fig = go.Figure()
    for _, r in df.iterrows():
        fig.add_trace(
            go.Scatter(
                x=["2025", "2026"],
                y=[r["y2025"], r["y2026"]],
                mode="lines+markers+text",
                name=r["bolge"],
                text=[None, r["bolge"]],
                textposition="middle right",
            )
        )
    fig.update_layout(yaxis_title="Ciro (M€)", showlegend=False)
    return style(fig)


@register(
    id="lollipop",
    title="Vadesi geçmiş alacaklar",
    plotly_type="Lollipop",
    module="FI",
    objects="BSID, FBL5N",
    use_case="Müşteri bazında overdue tutar.",
)
def chart_lollipop():
    df = pd.DataFrame(
        {"musteri": ["A101", "B205", "C018", "D440"], "overdue": [0.42, 0.31, 0.18, 0.09]}
    ).sort_values("overdue")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["overdue"], y=df["musteri"], mode="markers", marker=dict(size=14, color="#AA0808"), name="Overdue"))
    for _, r in df.iterrows():
        fig.add_shape(type="line", x0=0, x1=r["overdue"], y0=r["musteri"], y1=r["musteri"], line=dict(color="#D9D9D9", width=3))
    fig.update_layout(xaxis_title="Overdue (M€)", yaxis_title="Müşteri", showlegend=False)
    return style(fig)


@register(
    id="tornado",
    title="Marj duyarlılığı",
    plotly_type="Tornado",
    module="CO",
    objects="CK11N, CO-PA",
    use_case="Hammadde, işçilik, fiyat ve kurun marja etkisi.",
)
def chart_tornado():
    factors = ["Hammadde", "Satış fiyatı", "İşçilik", "Kur", "Enerji"]
    low = [-2.4, -1.1, -0.8, -0.6, -0.3]
    high = [2.1, 1.4, 0.5, 0.7, 0.2]
    fig = go.Figure()
    fig.add_trace(go.Bar(y=factors, x=low, orientation="h", name="Olumsuz", marker_color="#AA0808"))
    fig.add_trace(go.Bar(y=factors, x=high, orientation="h", name="Olumlu", marker_color="#256F3A"))
    fig.update_layout(barmode="overlay", xaxis_title="Marj etkisi (pp)", yaxis_title="Sürücü")
    return style(fig)


@register(
    id="aging-pyramid",
    title="Alacak yaşlandırma piramidi",
    plotly_type="Pyramid",
    module="FI",
    objects="BSID, FBL5N aging",
    use_case="Yurt içi / yurt dışı açık kalem yaşları.",
)
def chart_aging_pyramid():
    buckets = ["0-30", "31-60", "61-90", "90+"]
    yurtici = [2.4, 1.1, 0.5, 0.3]
    yurtdisi = [1.6, 0.8, 0.4, 0.2]
    fig = go.Figure()
    fig.add_trace(go.Bar(y=buckets, x=[-v for v in yurtici], name="Yurt içi", orientation="h", marker_color="#0070F2"))
    fig.add_trace(go.Bar(y=buckets, x=yurtdisi, name="Yurt dışı", orientation="h", marker_color="#E76500"))
    fig.update_layout(barmode="relative", xaxis_title="Açık bakiye (M€)", yaxis_title="Yaş (gün)")
    return style(fig)


@register(
    id="bump",
    title="Bölge ciro sıralaması",
    plotly_type="Bump",
    module="SD",
    objects="VBAK, T005",
    use_case="Aylık ciro sıralamasının değişimi.",
)
def chart_bump():
    months = ["Oca", "Şub", "Mar", "Nis"]
    ranks = {
        "Marmara": [1, 1, 1, 1],
        "Ege": [2, 3, 2, 2],
        "İç Anadolu": [3, 2, 3, 3],
        "Akdeniz": [4, 4, 4, 4],
    }
    fig = go.Figure()
    for name, r in ranks.items():
        fig.add_trace(go.Scatter(x=months, y=r, mode="lines+markers", name=name, marker=dict(size=10)))
    fig.update_yaxes(autorange="reversed", dtick=1, title="Sıra")
    fig.update_layout(xaxis_title="Ay")
    return style(fig)


# ---------------------------------------------------------------------------
# Polar / ternary
# ---------------------------------------------------------------------------


@register(
    id="radar",
    title="Tedarikçi skor kartı",
    plotly_type="Radar (scatterpolar)",
    module="MM",
    objects="ME61, vendor evaluation",
    use_case="Fiyat, kalite, teslimat, servis, inovasyon notları.",
)
def chart_radar():
    cats = ["Fiyat", "Kalite", "Teslimat", "Servis", "İnovasyon"]
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(r=[80, 90, 70, 85, 60], theta=cats, fill="toself", name="Bosch"))
    fig.add_trace(go.Scatterpolar(r=[70, 75, 90, 65, 80], theta=cats, fill="toself", name="Siemens"))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])))
    return style(fig, axes=False)


@register(
    id="barpolar",
    title="Aylık sipariş mevsimselliği",
    plotly_type="Bar polar",
    module="SD",
    objects="VBAK-ERDAT",
    use_case="Yılın aylarına göre sipariş hacmi (nightingale).",
)
def chart_barpolar():
    df = pd.DataFrame(
        {
            "ay": ["Oca", "Şub", "Mar", "Nis", "May", "Haz", "Tem", "Ağu", "Eyl", "Eki", "Kas", "Ara"],
            "siparis": [3.2, 3.0, 3.8, 3.6, 4.1, 4.4, 3.5, 3.3, 4.0, 4.2, 4.6, 3.9],
        }
    )
    fig = px.bar_polar(df, r="siparis", theta="ay", color="siparis", color_continuous_scale="Blues")
    fig.update_layout(coloraxis_showscale=False)
    return style(fig, axes=False)


@register(
    id="linepolar",
    title="Kapasite yük döngüsü",
    plotly_type="Line polar",
    module="PP",
    objects="KBED, CRHD",
    use_case="Haftalık kapasite kullanımının döngüsel görünümü.",
)
def chart_linepolar():
    df = pd.DataFrame(
        {
            "hafta": [f"W{i:02d}" for i in range(1, 13)],
            "yuk": [62, 70, 78, 85, 92, 88, 80, 74, 81, 90, 86, 68],
        }
    )
    fig = px.line_polar(df, r="yuk", theta="hafta", line_close=True)
    fig.update_traces(fill="toself")
    return style(fig, axes=False)


@register(
    id="ternary",
    title="Maliyet–süre–kalite üçgeni",
    plotly_type="Scatter ternary",
    module="PP",
    objects="AFKO, QMEL, KEKO",
    use_case="Ürün hatlarının üç kısıt üzerindeki konumu.",
)
def chart_ternary():
    df = pd.DataFrame(
        {
            "urun": ["FG-A", "FG-B", "FG-C", "FG-D"],
            "maliyet": [40, 25, 20, 35],
            "sure": [35, 40, 25, 20],
            "kalite": [25, 35, 55, 45],
        }
    )
    fig = px.scatter_ternary(df, a="maliyet", b="sure", c="kalite", color="urun", size=[12] * 4)
    return style(fig, axes=False)


# ---------------------------------------------------------------------------
# Maps / geo
# ---------------------------------------------------------------------------


@register(
    id="choropleth",
    title="Ülkeye göre net ciro",
    plotly_type="Choropleth",
    module="SD",
    objects="KNA1-LAND1, VBAK-NETWR",
    use_case="Müşteri ülkesine göre ciro haritası.",
    wide=True,
    height=460,
)
def chart_choropleth():
    df = pd.DataFrame(
        {
            "iso": ["DEU", "TUR", "USA", "FRA", "NLD", "ITA", "GBR", "ESP"],
            "ciro": [12.4, 8.1, 6.7, 4.2, 3.5, 2.8, 2.4, 1.9],
        }
    )
    fig = px.choropleth(df, locations="iso", color="ciro", color_continuous_scale="Blues")
    fig.update_geos(showcountries=True, projection_type="natural earth", showframe=False)
    fig.update_layout(coloraxis_colorbar=dict(title="M€"))
    return style(fig, height=460, axes=False)


@register(
    id="scatter-geo",
    title="Tesis ağı ve üretim hacmi",
    plotly_type="Scatter geo",
    module="PP",
    objects="T001W, AFPO",
    use_case="Üretim tesislerinin coğrafi dağılımı.",
    wide=True,
    height=460,
)
def chart_scatter_geo():
    df = pd.DataFrame(
        {
            "tesis": ["1010 München", "2010 İstanbul", "3010 İzmir", "4010 Stuttgart", "5010 Gaziantep"],
            "lat": [48.14, 41.01, 38.42, 48.78, 37.07],
            "lon": [11.58, 28.98, 27.14, 9.18, 37.38],
            "hacim": [420, 310, 180, 260, 140],
        }
    )
    fig = px.scatter_geo(df, lat="lat", lon="lon", size="hacim", hover_name="tesis", projection="natural earth")
    fig.update_geos(showcountries=True, lataxis_range=[35, 55], lonaxis_range=[-5, 45], showframe=False)
    return style(fig, height=460, axes=False)


@register(
    id="scatter-map",
    title="Sevkiyat noktaları",
    plotly_type="Scatter map",
    module="LE",
    objects="LIKP-KUNNR, ADRC",
    use_case="Teslimat adreslerinin harita üzerinde hacmi.",
    wide=True,
    height=460,
)
def chart_scatter_map():
    df = pd.DataFrame(
        {
            "nokta": ["İstanbul", "Ankara", "İzmir", "Bursa", "München", "Rotterdam"],
            "lat": [41.01, 39.93, 38.42, 40.18, 48.14, 51.92],
            "lon": [28.98, 32.85, 27.14, 29.06, 11.58, 4.48],
            "teslimat": [220, 90, 80, 70, 150, 110],
        }
    )
    fig = px.scatter_map(df, lat="lat", lon="lon", size="teslimat", hover_name="nokta", zoom=3)
    fig.update_layout(map_style="open-street-map")
    return style(fig, height=460, axes=False)


@register(
    id="density-map",
    title="Teslimat yoğunluğu",
    plotly_type="Density map",
    module="LE",
    objects="LIPS, VTTK",
    use_case="Sevkiyat yoğunluğunun ısı haritası.",
    wide=True,
    height=460,
)
def chart_density_map():
    rng = np.random.default_rng(15)
    # cluster around Istanbul, Munich, Izmir
    clusters = [(41.01, 28.98, 80), (48.14, 11.58, 50), (38.42, 27.14, 40)]
    lats, lons, z = [], [], []
    for lat, lon, n in clusters:
        lats.extend(rng.normal(lat, 0.35, n))
        lons.extend(rng.normal(lon, 0.45, n))
        z.extend(rng.integers(1, 6, n))
    df = pd.DataFrame({"lat": lats, "lon": lons, "adet": z})
    fig = px.density_map(df, lat="lat", lon="lon", z="adet", zoom=4, radius=18)
    fig.update_layout(map_style="open-street-map")
    return style(fig, height=460, axes=False)


# ---------------------------------------------------------------------------
# Tables / time / finance series
# ---------------------------------------------------------------------------


@register(
    id="table",
    title="Açık alacak yaşlandırma tablosu",
    plotly_type="Table",
    module="FI",
    objects="BSID, FBL5N",
    use_case="Müşteri açık kalemleri (ALV benzeri).",
    wide=True,
    height=300,
)
def chart_table():
    header = ["Müşteri", "Belge", "Tutar (€)", "Vade", "Yaş (gün)", "Durum"]
    cells = [
        ["A101", "A205", "B010", "C330"],
        ["1800000123", "1800000140", "1800000201", "1800000218"],
        ["42.000", "18.500", "9.200", "31.000"],
        ["2026-07-12", "2026-08-01", "2026-08-20", "2026-06-30"],
        ["50", "30", "11", "62"],
        ["Overdue", "Open", "Open", "Overdue"],
    ]
    fig = go.Figure(
        go.Table(
            header=dict(values=header, fill_color="#0070F2", font=dict(color="white"), align="left"),
            cells=dict(values=cells, fill_color="#F5F6F7", align="left"),
        )
    )
    return style(fig, height=300, axes=False)


@register(
    id="candlestick",
    title="EUR/TRY günlük kur",
    plotly_type="Candlestick",
    module="TR",
    objects="TCURR, TCURF",
    use_case="Hazine kur takibi (OHLC mum).",
    wide=True,
)
def chart_candlestick():
    dates = pd.date_range("2026-08-01", periods=12, freq="B")
    close = np.array([47.2, 47.4, 47.1, 47.6, 47.9, 47.5, 47.8, 48.1, 47.7, 48.0, 48.3, 48.1])
    fig = go.Figure(
        go.Candlestick(
            x=dates,
            open=close - 0.15,
            high=close + 0.35,
            low=close - 0.40,
            close=close,
        )
    )
    fig.update_layout(yaxis_title="EUR/TRY", xaxis_rangeslider_visible=False)
    return style(fig)


@register(
    id="ohlc",
    title="Bakır emtia fiyatı (OHLC)",
    plotly_type="OHLC",
    module="TR",
    objects="Hazine / MM emtia",
    use_case="Satınalma hammadde fiyat bandı.",
    wide=True,
)
def chart_ohlc():
    dates = pd.date_range("2026-08-01", periods=10, freq="B")
    close = np.array([9.1, 9.0, 9.3, 9.2, 9.5, 9.4, 9.6, 9.3, 9.7, 9.8])
    fig = go.Figure(
        go.Ohlc(
            x=dates,
            open=close - 0.08,
            high=close + 0.18,
            low=close - 0.16,
            close=close,
        )
    )
    fig.update_layout(yaxis_title="USD / kg", xaxis_rangeslider_visible=False)
    return style(fig)


@register(
    id="timeline",
    title="Proje WBS zaman planı",
    plotly_type="Timeline / Gantt",
    module="PS",
    objects="PROJ, PRPS, AFVC",
    use_case="WBS faaliyetlerinin Gantt görünümü (CJ20N).",
    wide=True,
    height=360,
)
def chart_timeline():
    df = pd.DataFrame(
        {
            "wbs": ["Mühendislik", "Satınalma", "İmalat", "Montaj", "Devreye alma"],
            "start": ["2026-01-06", "2026-02-10", "2026-03-17", "2026-06-02", "2026-07-14"],
            "finish": ["2026-02-28", "2026-04-15", "2026-06-20", "2026-07-20", "2026-08-15"],
        }
    )
    fig = px.timeline(df, x_start="start", x_end="finish", y="wbs", color="wbs")
    fig.update_yaxes(autorange="reversed")
    fig.update_layout(showlegend=False, xaxis_title="Tarih")
    return style(fig, height=360)


# ---------------------------------------------------------------------------
# 3D
# ---------------------------------------------------------------------------


@register(
    id="scatter3d",
    title="CO-PA: fiyat, hacim, marj",
    plotly_type="Scatter 3D",
    module="CO-PA",
    objects="CE1xxxx, ARTNR",
    use_case="Ürünlerin fiyat-hacim-marj uzayı.",
    height=460,
)
def chart_scatter3d():
    rng = np.random.default_rng(16)
    df = pd.DataFrame(
        {
            "fiyat": rng.uniform(20, 80, 30),
            "hacim": rng.uniform(100, 900, 30),
            "marj": rng.uniform(8, 32, 30),
            "hat": rng.choice(["A", "B"], 30),
        }
    )
    fig = px.scatter_3d(df, x="fiyat", y="hacim", z="marj", color="hat")
    fig.update_layout(scene=dict(xaxis_title="Fiyat", yaxis_title="Hacim", zaxis_title="Marj %"))
    return style(fig, height=460, axes=False)


@register(
    id="surface",
    title="Parti ve hacme göre birim maliyet yüzeyi",
    plotly_type="Surface 3D",
    module="CO",
    objects="CK11N, KEKO",
    use_case="Lot size × volume maliyet yüzeyi.",
    height=480,
    wide=True,
)
def chart_surface():
    lot = np.linspace(50, 500, 24)
    vol = np.linspace(1, 20, 24)
    L, V = np.meshgrid(lot, vol)
    z = 42 + 800 / L + 15 / V
    fig = go.Figure(go.Surface(x=lot, y=vol, z=z, colorscale="Teal"))
    fig.update_layout(
        scene=dict(xaxis_title="Parti", yaxis_title="Hacim (bin)", zaxis_title="€/adet"),
        margin=dict(l=10, r=10, t=10, b=10),
    )
    return style(fig, height=480, axes=False)


@register(
    id="line3d",
    title="Nakit–kur–faiz yolu",
    plotly_type="Line 3D",
    module="TR",
    objects="FF7A, TCURR",
    use_case="Haftalık nakit pozisyonu, kur ve faiz birlikte.",
    height=460,
)
def chart_line3d():
    t = np.arange(1, 13)
    df = pd.DataFrame({"hafta": t, "nakit": 12 + np.sin(t / 2) * 1.4, "kur": 47 + t * 0.08, "faiz": 42 - t * 0.3})
    fig = px.line_3d(df, x="nakit", y="kur", z="faiz")
    fig.update_layout(scene=dict(xaxis_title="Nakit (M€)", yaxis_title="EUR/TRY", zaxis_title="Faiz %"))
    return style(fig, height=460, axes=False)


# ---------------------------------------------------------------------------
# Small multiples / animation
# ---------------------------------------------------------------------------


@register(
    id="faceted",
    title="Bölümlere göre aylık ciro",
    plotly_type="Faceted small multiples",
    module="SD",
    objects="VBAK-SPART",
    use_case="Her satış bölümü için ayrı küçük grafik.",
    wide=True,
    height=360,
)
def chart_faceted():
    months = ["Oca", "Şub", "Mar", "Nis"]
    df = pd.DataFrame(
        {
            "ay": months * 3,
            "spart": ["Beyaz eşya"] * 4 + ["TV"] * 4 + ["Klima"] * 4,
            "ciro": [2.1, 2.0, 2.4, 2.3, 1.3, 1.4, 1.5, 1.4, 0.7, 0.8, 0.9, 1.0],
        }
    )
    fig = px.bar(df, x="ay", y="ciro", facet_col="spart", color="spart")
    fig.update_layout(showlegend=False, yaxis_title="Ciro (M€)")
    return style(fig, height=360)


@register(
    id="animated",
    title="Satış org. cirosunun aylık animasyonu",
    plotly_type="Animated bar",
    module="SD",
    objects="VBAK-VKORG, VBAK-ERDAT",
    use_case="Aylar arasında ciro değişiminin oynatılması.",
    wide=True,
)
def chart_animated():
    rows = []
    base = {"1000 DE": 12.0, "2000 TR": 8.0, "3000 US": 6.5, "4000 FR": 4.0}
    for i, ay in enumerate(["Oca", "Şub", "Mar", "Nis"]):
        for org, v in base.items():
            rows.append({"ay": ay, "vkorg": org, "ciro": round(v + i * 0.25 + (hash(org) % 3) * 0.05, 2)})
    df = pd.DataFrame(rows)
    fig = px.bar(df, x="vkorg", y="ciro", color="vkorg", animation_frame="ay", range_y=[0, 14])
    fig.update_layout(showlegend=False, yaxis_title="Ciro (M€)", xaxis_title="Satış organizasyonu")
    return style(fig)
