import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# -------------------------
# CONFIG
# -------------------------
st.set_page_config(page_title="Control Operativo — Ferries", layout="wide")

BASE = Path(__file__).resolve().parents[1]
REPORTS = BASE / "reports"

# -------------------------
# LOADERS
# -------------------------
@st.cache_data
def load_csv(name: str) -> pd.DataFrame:
    p = REPORTS / name
    if not p.exists():
        st.error(f"❌ Falta el archivo: {p}")
        st.stop()
    return pd.read_csv(p)

def fmt_int(x):
    try:
        return f"{int(x):,}".replace(",", ".")
    except:
        return str(x)

def fmt_float(x, nd=2):
    try:
        return f"{float(x):.{nd}f}"
    except:
        return str(x)

def kpi_card(col, title, value, delta=None, help_text=None):
    col.metric(title, value, delta=delta, help=help_text)

# -------------------------
# HEADER
# -------------------------
st.title("🚢 Control Operativo y Eficiencia — Ferries")
st.caption("Versión consultoría: Executive / Diagnosis / Control Tower")

if not REPORTS.exists():
    st.error("❌ No existe la carpeta `reports/` en esta rama.")
    st.stop()

# -------------------------
# DATA
# -------------------------
kpi = load_csv("kpi_executive_summary.csv")
route_ops = load_csv("route_ops_traffic_light.csv")
pareto = load_csv("pareto_delay_by_reason.csv")
hotspots = load_csv("hotspots_route_hour.csv")

# -------------------------
# SIDEBAR (Filters)
# -------------------------
st.sidebar.header("Filtros")

# Filtro por status (Control Tower)
status_options = ["ALL"] + sorted(route_ops["status"].dropna().unique().tolist())
status_sel = st.sidebar.selectbox("Estado ruta (semáforo)", status_options, index=0)

# Filtro por ruta
route_options = ["ALL"] + sorted(route_ops["route_id"].dropna().unique().tolist())
route_sel = st.sidebar.selectbox("Ruta", route_options, index=0)

# Top N causas
top_n = st.sidebar.slider("Top causas (Pareto)", 3, 10, 7)

st.sidebar.divider()
st.sidebar.caption("Si un filtro no aplica a una vista, se ignora.")

# -------------------------
# APPLY FILTERS (where possible)
# -------------------------
route_ops_f = route_ops.copy()

if status_sel != "ALL":
    route_ops_f = route_ops_f[route_ops_f["status"] == status_sel]

if route_sel != "ALL":
    route_ops_f = route_ops_f[route_ops_f["route_id"] == route_sel]

# hotspots sí tiene route_id
hotspots_f = hotspots.copy()
if route_sel != "ALL":
    hotspots_f = hotspots_f[hotspots_f["route_id"] == route_sel]

# -------------------------
# TABS
# -------------------------
tab_exec, tab_diag, tab_tower = st.tabs(["📌 Executive", "🧪 Diagnosis", "🚦 Control Tower"])

# =========================================================
# TAB 1 — EXECUTIVE
# =========================================================
with tab_exec:
    st.subheader("KPIs globales")
    row = kpi.iloc[0]

    c1, c2, c3, c4, c5 = st.columns(5)
    kpi_card(c1, "Servicios", fmt_int(row.get("services_total")))
    kpi_card(c2, "Completados", fmt_int(row.get("services_completed")))
    kpi_card(c3, "Cancel Rate", f"{fmt_float(row.get('cancel_rate_%'))}%")
    kpi_card(c4, "Delay medio", f"{fmt_float(row.get('avg_delay_min'))} min")
    kpi_card(c5, "P95 delay", f"{fmt_float(row.get('p95_delay_min'))} min")

    c6, c7, c8 = st.columns(3)
    kpi_card(c6, "Ocupación media", fmt_float(row.get("avg_occupancy"), 3))
    kpi_card(c7, "Margen medio", fmt_int(row.get("avg_margin")), help_text="Media de margen por servicio (sintético).")
    kpi_card(c8, "Margen total", fmt_int(row.get("total_margin")))

    st.divider()

    st.subheader("Resumen ejecutivo (qué priorizar)")
    # Top AMBER por delay
    amber = route_ops.sort_values(["status", "avg_delay"], ascending=[True, False])
    amber = amber[amber["status"].isin(["AMBER", "RED"])] if "RED" in amber["status"].unique() else amber[amber["status"]=="AMBER"]
    top_routes = amber.head(5)[["route_id", "on_time_15_%", "avg_delay", "p95_delay", "avg_margin", "status"]]

    # Top causas pareto
    pareto_sorted = pareto.sort_values("total_delay_min", ascending=False).head(top_n)

    left, right = st.columns([1, 1])
    with left:
        st.markdown("**Rutas prioritarias (semáforo)**")
        if len(top_routes) == 0:
            st.info("No hay rutas AMBER/RED con la regla actual.")
        else:
            st.dataframe(top_routes, use_container_width=True, hide_index=True)

    with right:
        st.markdown("**Top causas por retraso total (Pareto)**")
        st.dataframe(
            pareto_sorted[["disruption_reason", "share_%", "cum_share_%", "avg_delay_min", "p95_delay_min"]],
            use_container_width=True,
            hide_index=True
        )

# =========================================================
# TAB 2 — DIAGNOSIS
# =========================================================
with tab_diag:
    st.subheader("Pareto de retraso por causa")

    pareto_sorted = pareto.sort_values("total_delay_min", ascending=False)
    pareto_top = pareto_sorted.head(top_n)

    fig_pareto = px.bar(
        pareto_top,
        x="disruption_reason",
        y="total_delay_min",
        hover_data=["services", "avg_delay_min", "p95_delay_min", "share_%", "cum_share_%"],
        title="Total delay (min) por causa (Top N)"
    )
    st.plotly_chart(fig_pareto, use_container_width=True)

    st.divider()

    st.subheader("Hotspots: ruta × hora (delay medio)")
    if hotspots_f.empty:
        st.warning("No hay datos de hotspots para el filtro seleccionado.")
    else:
        pivot = hotspots_f.pivot_table(index="route_id", columns="hour", values="avg_delay", aggfunc="mean")
        pivot = pivot.reindex(columns=sorted(pivot.columns))

        fig_hm = px.imshow(
            pivot,
            aspect="auto",
            labels=dict(x="Hora", y="Ruta", color="Delay (min)"),
            title="Heatmap de delay medio (min)"
        )
        st.plotly_chart(fig_hm, use_container_width=True)

        # Tabla de peores combinaciones (acción)
        st.markdown("**Top combinaciones ruta-hora (por delay medio)**")
        top_hot = (hotspots_f.sort_values("avg_delay", ascending=False)
                   .head(10)[["route_id", "hour", "avg_delay", "p95_delay", "on_time_15_%"]])
        st.dataframe(top_hot, use_container_width=True, hide_index=True)

# =========================================================
# TAB 3 — CONTROL TOWER
# =========================================================
with tab_tower:
    st.subheader("Semáforo de rutas (operación semanal)")
    st.caption("Filtra por ruta/estado en la barra lateral. Objetivo: detectar dónde actuar primero.")

    # Scatter: delay vs margin
    fig_routes = px.scatter(
        route_ops_f,
        x="avg_delay",
        y="avg_margin",
        size="services",
        color="status",
        hover_data=["route_id", "on_time_15_%", "p95_delay"],
        title="Balance operativo: Delay vs Margen (tamaño = volumen)"
    )
    st.plotly_chart(fig_routes, use_container_width=True)

    st.markdown("**Tabla Control Tower**")
    cols = ["route_id", "status", "services", "on_time_15_%", "avg_delay", "p95_delay", "avg_margin"]
    # Si alguna columna no existe por formato, no rompemos:
    cols = [c for c in cols if c in route_ops_f.columns]

    st.dataframe(
        route_ops_f.sort_values(["status", "avg_delay"], ascending=[True, False])[cols],
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    st.subheader("Alertas (reglas simples)")
    st.caption("Reglas tipo ‘operación real’: umbrales directos (no cuartiles). Ajusta para tu narrativa.")

    colA, colB, colC = st.columns(3)
    with colA:
        thr_otr = st.slider("OTR(15) mínimo (%)", 40, 95, 70)
    with colB:
        thr_p95 = st.slider("P95 máximo (min)", 20, 120, 45)
    with colC:
        thr_delay = st.slider("Delay medio máximo (min)", 5, 40, 14)

    alert = route_ops.copy()
    if route_sel != "ALL":
        alert = alert[alert["route_id"] == route_sel]
    if status_sel != "ALL":
        alert = alert[alert["status"] == status_sel]

    # Convertimos a números por si vienen como strings
    for c in ["on_time_15_%", "p95_delay", "avg_delay"]:
        if c in alert.columns:
            alert[c] = pd.to_numeric(alert[c], errors="coerce")

    alert = alert[
        (alert["on_time_15_%"] < thr_otr) |
        (alert["p95_delay"] > thr_p95) |
        (alert["avg_delay"] > thr_delay)
    ].sort_values(["status", "avg_delay"], ascending=[True, False])

    if alert.empty:
        st.success("✅ Sin alertas con los umbrales actuales.")
    else:
        st.warning("⚠️ Rutas en alerta (según umbrales)")
        st.dataframe(
            alert[["route_id", "status", "services", "on_time_15_%", "avg_delay", "p95_delay", "avg_margin"]],
            use_container_width=True,
            hide_index=True
        )

st.caption("Datos: outputs sintéticos generados en notebooks y exportados a /reports.")
