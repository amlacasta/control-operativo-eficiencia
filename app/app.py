import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="Control Operativo — Ferries", layout="wide")

BASE = Path(__file__).resolve().parents[1]
REPORTS = BASE / "reports"

@st.cache_data
def load_csv(name: str) -> pd.DataFrame:
    p = REPORTS / name
    if not p.exists():
        st.error(f"Falta el archivo: {p}")
        st.stop()
    return pd.read_csv(p)

st.title("🚢 Control Operativo y Eficiencia — Ferries")

kpi = load_csv("kpi_executive_summary.csv")
route_ops = load_csv("route_ops_traffic_light.csv")
pareto = load_csv("pareto_delay_by_reason.csv")
hotspots = load_csv("hotspots_route_hour.csv")

st.subheader("📊 KPIs Globales")
row = kpi.iloc[0]
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Servicios", f"{int(row['services_total']):,}")
c2.metric("Completados", f"{int(row['services_completed']):,}")
c3.metric("Cancel Rate", f"{row['cancel_rate_%']:.2f}%")
c4.metric("Delay medio", f"{row['avg_delay_min']:.2f} min")
c5.metric("P95 delay", f"{row['p95_delay_min']:.2f} min")

st.divider()

st.subheader("🚦 Control Tower — Rutas")
fig_routes = px.scatter(
    route_ops,
    x="avg_delay",
    y="avg_margin",
    size="services",
    color="status",
    hover_data=["route_id", "on_time_15_%", "p95_delay"],
    title="Delay vs Margen (tamaño = servicios)"
)
st.plotly_chart(fig_routes, use_container_width=True)
st.dataframe(route_ops.sort_values(["status", "avg_delay"], ascending=[True, False]),
             use_container_width=True, hide_index=True)

st.divider()

st.subheader("📈 Pareto de retraso por causa")
pareto_sorted = pareto.sort_values("total_delay_min", ascending=False)
fig_pareto = px.bar(pareto_sorted, x="disruption_reason", y="total_delay_min",
                    hover_data=["services","avg_delay_min","p95_delay_min","share_%"],
                    title="Total delay (min) por causa")
st.plotly_chart(fig_pareto, use_container_width=True)

st.divider()

st.subheader("🔥 Hotspots ruta × hora (delay medio)")
pivot = hotspots.pivot_table(index="route_id", columns="hour", values="avg_delay", aggfunc="mean")
fig_hm = px.imshow(pivot, aspect="auto", labels=dict(x="Hora", y="Ruta", color="Delay (min)"))
st.plotly_chart(fig_hm, use_container_width=True)
