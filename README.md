Control Operativo y Eficiencia — Ferries
1) Objetivo
Construir un sistema de control operativo para una red de rutas de ferris que permita: - medir puntualidad (OTR), retrasos, ocupación y rentabilidad, - detectar rutas/horas/circunstancias problemáticas, - priorizar acciones operativas basadas en datos.

2) Alcance
Dataset sintético realista (reproducible) de operaciones de ferris.
KPIs globales y segmentados por ruta, hora, clima y causa de disrupción.
Diagnóstico (Pareto de causas, interacción clima–causa, hotspots temporales).
Recomendaciones operativas accionables + semáforo tipo “Control Tower”.
Nota: El dataset es sintético y se genera automáticamente para simular escenarios realistas sin usar datos sensibles.

3) Dataset
3.1 Generación
El dataset se genera en: - notebooks/01_generate_dataset.ipynb

Salida: - ferry_operations_raw.csv (no se versiona en Git por tamaño/buenas prácticas)

3.2 Estructura (columnas principales)
operation_id: identificador del servicio
route_id, origin, destination
scheduled_start, actual_start, scheduled_end, actual_end
delay_min, cycle_time_min, on_time, canceled
weather, disruption_reason, maintenance_flag
vessel_type, capacity_pax, passengers, occupancy
revenue, total_cost, margin
4) KPIs (definiciones)
Cancel Rate = % servicios cancelados
On-Time Rate (OTR) = % servicios con delay_min ≤ threshold (sobre no cancelados)
Average Delay = media de delay_min
P95 Delay = percentil 95 de delay_min
Occupancy = passengers / capacity_pax
Margin = revenue - total_cost
5) Resultados (Executive Summary)
Servicios totales: 12,000
Servicios completados: 11,814
Cancel Rate: 1.55%
OTR (≤5 min): 33.16%
Delay medio: 11.83 min
P95 delay: 36.14 min
Ocupación media: 0.577
Margen medio: 27,141
Margen total: 3.206e+08
5.1 Rutas con mayor retraso medio
BCN–IBZ (avg delay: 15.18)
VAL–IBZ (avg delay: 15.02)
VAL–PMI (avg delay: 14.84)
BCN–PMI (avg delay: 14.41)
DEN–PMI (avg delay: 12.15)
5.2 Puntualidad (sensibilidad del umbral)
OTR ≤ 5 min: 33.16%
OTR ≤ 15 min: 73.93%
Interpretación: en ferris, 5 minutos es un umbral muy estricto; 15 minutos ofrece una lectura más alineada con la realidad operativa.

5.3 Priorización por Balance Score (delay vs margen vs ocupación)
Rutas más saludables: DEN–FOR, DEN–IBZ
Rutas a priorizar: VAL–PMI, BCN–PMI, VAL–IBZ, ALG–PMI, BCN–IBZ
6) Diagnóstico (insights)
6.1 Pareto de retraso total
WEATHER aporta el 28.44% del retraso total.
TECHNICAL aporta el 16.27%.
PORT_CONGESTION aporta el 14.14%.
Con WEATHER + TECHNICAL se explica el 44.71% del retraso; añadiendo PORT_CONGESTION se alcanza ~74.95%.
6.2 Interacción clima–causa
En ROUGH/STORM el retraso medio se dispara, especialmente cuando coincide con TECHNICAL o WEATHER:
ROUGH: TECHNICAL ~27.6 min, WEATHER ~25.0 min (P95 > 65 min).
STORM: TECHNICAL ~42.6 min (P95 ~105 min), WEATHER ~40.4 min (P95 ~87 min).
Conclusión: el clima severo amplifica las disrupciones; la gestión por umbrales meteo es una palanca crítica.
6.3 Hotspots operativos (ruta × hora)
Se observan combinaciones de alta demora concentradas en rutas como BCN–IBZ y VAL–IBZ/VAL–PMI, con franjas problemáticas entre 09:00–11:00 y 14:00–21:00.
En los hotspots, el OTR ≤ 15 min cae a ~52–64%, indicando retraso sistemático en ventanas específicas.
7) Recomendaciones operativas
1) Plan de contingencia por meteo (WEATHER) - Definir umbrales operativos (WINDY/ROUGH/STORM) con acciones: buffer adicional, ajuste de slot, refuerzo de personal de embarque y comunicación al cliente. - Justificación: WEATHER es la principal fuente de retraso agregado. Reducir 10% WEATHER ahorra ~2.84% del retraso total; combinado con TECHNICAL llega a ~4.47%.

2) Fiabilidad técnica (TECHNICAL) - Refuerzo de mantenimiento preventivo y checks pre-salida en rutas con peor desempeño (AMBER), especialmente en condiciones ROUGH/STORM. - Justificación: TECHNICAL aporta una parte relevante del retraso y se amplifica con mal clima (colas P95 altas).

3) Gestión de congestión de puerto (PORT_CONGESTION) - Ajustar buffers y ventanas de atraque en franjas problemáticas; coordinación con autoridad portuaria y revisión de turnos en picos. - Impacto estimado: reducir 10% PORT_CONGESTION ahorra ~1.41% del retraso total.

4) Control Tower: semáforo de rutas - Rutas prioridad (AMBER): BCN–IBZ, VAL–IBZ, VAL–PMI, BCN–PMI (OTR ≤15 min ~64–66%). - Rutas saludables (GREEN): DEN–FOR, DEN–IBZ (OTR ≤15 min ~89%). - Uso: revisar semanalmente OTR(15), delay medio y P95; activar acciones correctivas en AMBER.

8) Outputs del proyecto
reports/executive_summary.md: resumen ejecutivo (1 página).
reports/figures/: Pareto, heatmap ruta×hora y boxplot por clima.
reports/*.csv: tablas exportadas (KPIs, rutas, hotspots, semáforo).
9) Cómo reproducir (Google Colab)
Abrir notebooks/01_generate_dataset.ipynb y ejecutarlo (genera el CSV raw local).
Ejecutar notebooks/02_profiling_kpis.ipynb (KPIs + ranking + semáforo).
Ejecutar notebooks/03_diagnostics.ipynb (Pareto, hotspots, visualizaciones + exports a reports/).
10) Estructura del repositorio
```text control-operativo-ferries/ ├─ data/ │ ├─ raw/ │ └─ processed/ ├─ notebooks/ │ ├─ 01_generate_dataset.ipynb │ ├─ 02_profiling_kpis.ipynb │ └─ 03_diagnostics.ipynb ├─ src/ ├─ reports/ │ ├─ figures/ │ └─ executive_summary.md └─ README.md
