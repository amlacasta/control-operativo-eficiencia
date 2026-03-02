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
        return f"{int(float(x)):,}".replace(",", ".")
    except:
        return str(x)

def fmt_float(x, nd=2):
    try:
        return f"{float(x):.{nd}f}"
    except:
        return str(x)

def kpi_card(col, title, value, delta=None, help_text=None):
    col.metric(title, value, delta=delta, help=help_text)

def best_otr_col(df: pd.DataFrame, thr: int) -> str | None:
    """
    Devuelve el nombre de columna OTR disponible más adecuada.
    Prioriza on_time_{thr}_% y si no existe, usa on_time_15_% si existe.
    """
    cand = f"on_time_{thr}_%"
    if cand in df.columns:
        return cand
    # fallback típico
    if "on_time_15_%" in df.columns:
        return "on_time_15_%"
    if "on_time_rate_%" in df.columns:
        return "on_time_rate_%"
    return None

def download_csv_button(df: pd.DataFrame, label: str, filename: str):
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(label=label, data=csv, file_name=filename, mime="text/csv")

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

otr_thr = st.sidebar.radio("Umbral OTR (min)", [5, 15], index=1)

status_options = ["ALL"] + sorted(route_ops["status"].dropna().unique().tolist())
status_sel = st.sidebar.selectbox("Estado ruta (semáforo)", status_options, index=0)

route_options = ["ALL"] + sorted(route_ops["route_id"].dropna().unique().tolist())
route_sel = st.sidebar.selectbox("Ruta", route_options, index=0)

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

hotspots_f = hotspots.copy()
if route_sel != "ALL":
    hotspots_f = hotspots_f[hotspots_f["route_id"] == route_sel]

# OTR column selection for route_ops (may fallback)
otr_col = best_otr_col(route_ops, otr_thr)
otr_label = f"OTR ≤ {otr_thr} min (%)"
if otr_col is None:
    otr_label = f"OTR (no disponible en CSV)"

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

    # KPI OTR (si existe info en kpi csv)
    # Tu kpi_executive_summary.csv tiene on_time_rate_% (según tu captura inicial). Eso es OTR a un umbral fijo (probablemente 5).
    # Mostramos ese KPI como "OTR (dataset)" y aclaramos el umbral elegido.
    c6, c7, c8, c9 = st.columns(4)
    kpi_card(c6, "Ocupación media", fmt_float(row.get("avg_occupancy"), 3))
    kpi_card(c7, "Margen medio", fmt_int(row.get("avg_margin")), help_text="Media de margen por servicio (sintético).")
    kpi_card(c8, "Margen total", fmt_int(row.get("total_margin")))
    if "on_time_rate_%" in kpi.columns:
        kpi_card(
            c9,
            "OTR (global)",
            f"{fmt_float(row.get('on_time_rate_%'))}%",
            help_text="OTR global del dataset (según tu pipeline). El umbral de Control Tower se elige en el sidebar."
        )
    else:
        kpi_card(c9, "OTR (global)", "N/A")

    st.divider()

    st.subheader("Resumen ejecutivo (qué priorizar)")

    # Top rutas con peor desempeño (AMBER/RED si existe)
    amber = route_ops.sort_values(["status", "avg_delay"], ascending=[True, False])
    if "RED" in amber["status"].unique():
        amber = amber[amber["status"].isin(["AMBER", "RED"])]
    else:
        amber = amber[amber["status"] == "AMBER"]
    top_routes = amber.head(5)

    cols_show = ["route_id", "status", "avg_delay", "p95_delay", "avg_margin"]
    if otr_col is not None and otr_col in top_routes.columns:
        cols_show.insert(2, otr_col)

    top_routes = top_routes[[c for c in cols_show if c in top_routes.columns]]

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

    st.divider()

    # ---------------------------------------
    # TOP 5 ACCIONES RECOMENDADAS (dinámicas)
    # ---------------------------------------
    st.subheader("Top 5 acciones recomendadas (automático)")

    # 1) acciones por Pareto
    top_causes = pareto_sorted["disruption_reason"].head(3).tolist()
    # 2) rutas en riesgo (por status o por delay)
    risky = route_ops.sort_values(["status", "avg_delay"], ascending=[True, False]).head(3)["route_id"].tolist()

    actions = []
    if "WEATHER" in top_causes:
        actions.append("Implementar **plan de contingencia meteo** (buffers por ROUGH/STORM, comunicación, slots).")
    if "TECHNICAL" in top_causes:
        actions.append("Refuerzo de **preventivo técnico** en rutas prioritarias + checklist pre-salida en días ROUGH/STORM.")
    if "PORT_CONGESTION" in top_causes:
        actions.append("Mitigar **congestión de puerto**: buffers por franja + coordinación de atraques en horas pico.")
    if "LATE_BOARDING" in top_causes:
        actions.append("Optimizar **embarque**: refuerzo de personal, señalización, corte de embarque y control de colas.")
    if "CREW" in top_causes:
        actions.append("Revisar **dimensionamiento de tripulación** en picos y rediseño de turnos/franjas críticas.")
    if "SECURITY" in top_causes:
        actions.append("Coordinar con seguridad para **fast-lane** en picos y pre-chequeos en horas de mayor demanda.")
    if "SUPPLY_ISSUE" in top_causes:
        actions.append("Mejorar **suministros**: stock mínimo y control preventivo en rutas con alta rotación.")

    # Acción transversal siempre útil
    actions.append(f"Activar **Control Tower semanal**: revisar OTR({otr_thr}), delay medio y P95; foco en rutas {', '.join(risky)}.")

    # Top 5 y sin duplicados
    actions_clean = []
    for a in actions:
        if a not in actions_clean:
            actions_clean.append(a)
    actions_clean = actions_clean[:5]

    for i, a in enumerate(actions_clean, 1):
        st.markdown(f"{i}. {a}")

    # Descargas rápidas (executive)
    st.divider()
    st.subheader("Descargas rápidas")
    d1, d2, d3, d4 = st.columns(4)
    with d1:
        download_csv_button(kpi, "⬇️ KPI global (CSV)", "kpi_executive_summary.csv")
    with d2:
        download_csv_button(route_ops_f, "⬇️ Rutas filtradas (CSV)", "route_ops_filtered.csv")
    with d3:
        download_csv_button(pareto_sorted, "⬇️ Pareto (CSV)", "pareto_delay_by_reason.csv")
    with d4:
        download_csv_button(hotspots_f, "⬇️ Hotspots filtrados (CSV)", "hotspots_filtered.csv")

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

        st.markdown("**Top combinaciones ruta-hora (por delay medio)**")
        # columnas pueden variar; seleccionamos las que existan
        base_cols = ["route_id", "hour", "avg_delay", "p95_delay", "on_time_15_%"]
        cols = [c for c in base_cols if c in hotspots_f.columns]
        top_hot = hotspots_f.sort_values("avg_delay", ascending=False).head(10)[cols]
        st.dataframe(top_hot, use_container_width=True, hide_index=True)

    st.divider()
    st.subheader("Descargas (Diagnosis)")
    dd1, dd2 = st.columns(2)
    with dd1:
        download_csv_button(pareto_top, "⬇️ Pareto Top N (CSV)", "pareto_top.csv")
    with dd2:
        if not hotspots_f.empty:
            download_csv_button(hotspots_f, "⬇️ Hotspots (CSV)", "hotspots.csv")

# =========================================================
# TAB 3 — CONTROL TOWER
# =========================================================
with tab_tower:
    st.subheader("Semáforo de rutas (operación semanal)")
    st.caption("Filtra por ruta/estado en la barra lateral. Objetivo: decidir dónde actuar primero.")

    # Scatter: delay vs margin
    fig_routes = px.scatter(
        route_ops_f,
        x="avg_delay",
        y="avg_margin",
        size="services",
        color="status",
        hover_data=["route_id"] + ([otr_col] if (otr_col is not None and otr_col in route_ops_f.columns) else []) + ["p95_delay"],
        title="Balance operativo: Delay vs Margen (tamaño = volumen)"
    )
    st.plotly_chart(fig_routes, use_container_width=True)

    st.markdown("**Tabla Control Tower**")
    cols = ["route_id", "status", "services"]
    if otr_col is not None and otr_col in route_ops_f.columns:
        cols.append(otr_col)
    # siempre que existan
    for c in ["avg_delay", "p95_delay", "avg_margin"]:
        if c in route_ops_f.columns:
            cols.append(c)

    st.dataframe(
        route_ops_f.sort_values(["status", "avg_delay"], ascending=[True, False])[cols],
        use_container_width=True,
        hide_index=True
    )

    # ---------------------------------------
    # ALERTAS con OTR elegido
    # ---------------------------------------
    st.divider()
    st.subheader("Alertas (reglas simples)")

    colA, colB, colC = st.columns(3)

    # Si no tenemos columna OTR adecuada, lo avisamos y usamos on_time_15_% si existe
    if otr_col is None or otr_col not in route_ops.columns:
        st.warning("No encuentro una columna de OTR en `route_ops_traffic_light.csv`. Añade `on_time_5_%`/`on_time_15_%` o `on_time_rate_%` para alertas por OTR.")
        thr_otr = None
    else:
        with colA:
            thr_otr = st.slider(f"{otr_label} mínimo", 40, 95, 70)

    with colB:
        thr_p95 = st.slider("P95 máximo (min)", 20, 120, 45)
    with colC:
        thr_delay = st.slider("Delay medio máximo (min)", 5, 40, 14)

    alert = route_ops.copy()
    if route_sel != "ALL":
        alert = alert[alert["route_id"] == route_sel]
    if status_sel != "ALL":
        alert = alert[alert["status"] == status_sel]

    # Convertimos a números
    for c in [otr_col, "p95_delay", "avg_delay"]:
        if c is not None and c in alert.columns:
            alert[c] = pd.to_numeric(alert[c], errors="coerce")

    conds = []
    if thr_otr is not None and otr_col is not None and otr_col in alert.columns:
        conds.append(alert[otr_col] < thr_otr)
    if "p95_delay" in alert.columns:
        conds.append(alert["p95_delay"] > thr_p95)
    if "avg_delay" in alert.columns:
        conds.append(alert["avg_delay"] > thr_delay)

    if len(conds) > 0:
        mask = conds[0]
        for c in conds[1:]:
            mask = mask | c
        alert = alert[mask].sort_values(["status", "avg_delay"], ascending=[True, False])
    else:
        alert = alert.iloc[0:0]

    if alert.empty:
        st.success("✅ Sin alertas con los umbrales actuales.")
    else:
        st.warning("⚠️ Rutas en alerta (según umbrales)")
        show_cols = ["route_id", "status", "services"]
        if otr_col is not None and otr_col in alert.columns:
            show_cols.append(otr_col)
        for c in ["avg_delay", "p95_delay", "avg_margin"]:
            if c in alert.columns:
                show_cols.append(c)

        st.dataframe(alert[show_cols], use_container_width=True, hide_index=True)

        st.markdown("**Descargar alertas**")
        download_csv_button(alert[show_cols], "⬇️ Alertas (CSV)", "alerts.csv")

st.caption("Datos: outputs sintéticos generados en notebooks y exportados a /reports.")
