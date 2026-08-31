"""SAP Fiori Horizon-inspired Plotly theme helpers."""

SAP_COLORS = [
    "#0070F2",
    "#E76500",
    "#256F3A",
    "#AA0808",
    "#5D36FF",
    "#07838F",
    "#C35500",
    "#188918",
    "#A100C2",
    "#0073AA",
]

FONT = "72, 'IBM Plex Sans', 'Segoe UI', sans-serif"


def style(fig, height=380, axes=True):
    fig.update_layout(
        template="plotly_white",
        font=dict(family=FONT, size=12, color="#1D2D3E"),
        colorway=SAP_COLORS,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#FFFFFF",
        margin=dict(l=52, r=28, t=28, b=44),
        height=height,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0, bgcolor="rgba(0,0,0,0)"),
        hoverlabel=dict(bgcolor="white", font_size=12, font_family=FONT),
        title=None,
    )
    if axes:
        fig.update_xaxes(
            showgrid=True,
            gridcolor="#EAECEE",
            zeroline=False,
            linecolor="#D9D9D9",
            ticks="outside",
            tickcolor="#D9D9D9",
        )
        fig.update_yaxes(
            showgrid=True,
            gridcolor="#EAECEE",
            zeroline=False,
            linecolor="#D9D9D9",
            ticks="outside",
            tickcolor="#D9D9D9",
        )
    return fig
