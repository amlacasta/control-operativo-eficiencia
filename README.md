# Control Operativo y Eficiencia — Ferries

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-lightgrey)
![Operations](https://img.shields.io/badge/Use%20Case-Operations%20Analytics-green)
![Control Tower](https://img.shields.io/badge/Control%20Tower-Sem%C3%A1foro%20Operativo-orange)
![Dashboard](https://img.shields.io/badge/Dashboard-GitHub%20Pages-brightgreen)
![Status](https://img.shields.io/badge/Status-Portfolio%20Project-success)

## Dashboard interactivo

El proyecto incluye un dashboard HTML interactivo publicado con GitHub Pages:

[**Abrir dashboard Control Operativo Ferries**](https://amlacasta.github.io/control-operativo-eficiencia/dashboard/dashboard_control_operativo_ferries.html)

El dashboard permite cargar el CSV operativo del proyecto y explorar KPIs, puntualidad, retrasos, rutas críticas, causas de disrupción, clima, hotspots ruta × hora y semáforo operativo.

Archivo recomendado para cargar:

```text
ferry_operations_raw.csv
```

---

## 1. Resumen ejecutivo

Este proyecto desarrolla un sistema de **control operativo y eficiencia** para una red ficticia de rutas de ferries.

El objetivo es transformar datos operativos de servicios marítimos en una herramienta de diagnóstico que permita:

- medir puntualidad,
- analizar retrasos,
- detectar rutas problemáticas,
- evaluar ocupación y rentabilidad,
- identificar causas principales de disrupción,
- y priorizar acciones mediante una lógica de **Control Tower**.

El proyecto trabaja con un dataset sintético pero realista de **12.000 servicios de ferry**, simulando rutas, horarios, retrasos, cancelaciones, condiciones meteorológicas, capacidad, pasajeros, ingresos, costes y margen.

Principales resultados globales:

| Indicador | Valor |
|---|---:|
| Servicios totales | 12.000 |
| Servicios completados | 11.814 |
| Cancel Rate | 1,55% |
| OTR ≤ 5 min | 33,16% |
| OTR ≤ 15 min | 73,93% |
| Delay medio | 11,83 min |
| P95 delay | 36,14 min |
| Ocupación media | 0,577 |
| Margen medio | 27.141 |
| Margen total | 320,6 M |

El análisis identifica como principales focos de mejora las rutas **BCN–IBZ**, **VAL–IBZ**, **VAL–PMI** y **BCN–PMI**, junto con causas operativas como **WEATHER**, **TECHNICAL** y **PORT_CONGESTION**.

---

## 2. Contexto de negocio

En una operación de ferries, la eficiencia depende de múltiples factores:

- puntualidad de salida y llegada,
- gestión de retrasos,
- meteorología,
- congestión portuaria,
- incidencias técnicas,
- ocupación de pasajeros,
- capacidad del buque,
- ingresos y costes operativos,
- y margen por servicio o ruta.

El problema no es únicamente saber si una ruta va tarde, sino entender:

```text
qué rutas fallan + cuándo fallan + por qué fallan + cuánto impactan en negocio
```

Este proyecto convierte datos operativos dispersos en una lectura estructurada para la toma de decisiones.

---

## 3. Objetivo del proyecto

Construir un sistema analítico que permita evaluar el rendimiento operativo de una red de ferries y priorizar acciones de mejora.

Objetivos específicos:

- calcular KPIs operativos globales y por ruta,
- medir puntualidad con diferentes umbrales,
- analizar retrasos medios y retrasos extremos,
- identificar causas principales de disrupción,
- estudiar la interacción entre clima y retrasos,
- localizar hotspots ruta × hora,
- evaluar ocupación y margen,
- generar un semáforo operativo de rutas,
- y proponer recomendaciones accionables.

---

## 4. Preguntas de negocio

El proyecto busca responder a preguntas como:

- ¿Cuál es la puntualidad real de la operación?
- ¿Qué rutas acumulan mayor retraso?
- ¿Qué causas explican la mayor parte del retraso total?
- ¿Qué ocurre cuando el mal clima se combina con incidencias técnicas?
- ¿Qué franjas horarias concentran más problemas?
- ¿Qué rutas son saludables y cuáles deben priorizarse?
- ¿Qué acciones podrían reducir el retraso agregado?
- ¿Cómo se puede convertir el diagnóstico en una torre de control operativa?

---

## 5. Dataset

Por motivos de confidencialidad, el proyecto utiliza un dataset **sintético y reproducible**, diseñado para simular escenarios realistas de una red de ferries.

### 5.1 Unidad de análisis

```text
1 fila = 1 servicio / operación de ferry
```

Cada registro representa un servicio programado con información de tiempos, ruta, estado operativo, ocupación e impacto económico.

### 5.2 Volumen

| Elemento | Valor |
|---|---:|
| Servicios simulados | 12.000 |
| Servicios completados | 11.814 |
| Servicios cancelados | 186 |

### 5.3 Variables principales

| Categoría | Variables |
|---|---|
| Identificación | `operation_id`, `route_id`, `origin`, `destination` |
| Planificación | `scheduled_start`, `scheduled_end` |
| Ejecución | `actual_start`, `actual_end`, `delay_min`, `cycle_time_min` |
| Estado | `on_time`, `canceled` |
| Disrupción | `weather`, `disruption_reason`, `maintenance_flag` |
| Capacidad | `vessel_type`, `capacity_pax`, `passengers`, `occupancy` |
| Economía | `revenue`, `total_cost`, `margin` |

---

## 6. Estructura del repositorio

```text
control-operativo-eficiencia/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── notebooks/
│   ├── 01_generate_dataset.ipynb
│   ├── 02_profiling_kpis.ipynb
│   └── 03_diagnostics.ipynb
│
├── reports/
│   ├── figures/
│   └── executive_summary.md
│
├── dashboard/
│   └── dashboard_control_operativo_ferries.html
│
├── src/
├── README.md
└── .gitignore
```

---

## 7. Metodología

El proyecto sigue un flujo analítico completo:

```text
datos sintéticos → KPIs → diagnóstico → semáforo → recomendaciones → dashboard
```

| Notebook | Objetivo | Output principal |
|---|---|---|
| `01_generate_dataset.ipynb` | Generar dataset sintético de operaciones | `ferry_operations_raw.csv` |
| `02_profiling_kpis.ipynb` | Calcular KPIs, rankings y semáforo | Tablas KPI y resumen operativo |
| `03_diagnostics.ipynb` | Analizar causas, hotspots y visualizaciones | Figuras y tablas de diagnóstico |

---

## 8. KPIs definidos

| KPI | Definición | Uso operativo |
|---|---|---|
| Cancel Rate | % de servicios cancelados | Medir fiabilidad de la operación |
| OTR ≤ 5 min | % de servicios con retraso menor o igual a 5 min | Lectura estricta de puntualidad |
| OTR ≤ 15 min | % de servicios con retraso menor o igual a 15 min | Lectura operativa más realista |
| Average Delay | Media de `delay_min` | Medir retraso promedio |
| P95 Delay | Percentil 95 del retraso | Capturar retrasos extremos |
| Occupancy | `passengers / capacity_pax` | Medir uso de capacidad |
| Margin | `revenue - total_cost` | Evaluar rentabilidad operativa |

---

## 9. Resultados globales

| Indicador | Valor |
|---|---:|
| Servicios totales | 12.000 |
| Servicios completados | 11.814 |
| Cancel Rate | 1,55% |
| Delay medio | 11,83 min |
| P95 delay | 36,14 min |
| Ocupación media | 0,577 |
| Margen medio | 27.141 |
| Margen total | 320,6 M |

### 9.1 Puntualidad según umbral

| Umbral OTR | Valor |
|---|---:|
| OTR ≤ 5 min | 33,16% |
| OTR ≤ 15 min | 73,93% |

La comparación muestra que un umbral de 5 minutos resulta muy estricto para una operación marítima. El umbral de 15 minutos ofrece una lectura más alineada con la realidad operativa de ferries.

---

## 10. Ranking de rutas por retraso

| Ruta | Delay medio | P95 delay | OTR ≤ 5 min | Margen medio |
|---|---:|---:|---:|---:|
| BCN–IBZ | 15,18 | 44,30 | 23,32% | 25.818 |
| VAL–IBZ | 15,02 | 44,75 | 22,96% | 25.981 |
| VAL–PMI | 14,84 | 42,88 | 24,81% | 24.006 |
| BCN–PMI | 14,41 | 40,14 | 24,03% | 23.683 |
| DEN–PMI | 12,15 | 34,56 | 29,96% | 28.622 |

### Interpretación

Las rutas **BCN–IBZ**, **VAL–IBZ**, **VAL–PMI** y **BCN–PMI** concentran mayor presión operativa. Presentan mayor retraso medio, colas de retraso elevadas y menor puntualidad estricta.

---

## 11. Diagnóstico de causas

### 11.1 Pareto de retraso total

| Causa | Share retraso total | Share acumulado | Delay medio | P95 delay |
|---|---:|---:|---:|---:|
| WEATHER | 28,44% | 28,44% | 18,29 | 49,90 |
| TECHNICAL | 16,27% | 44,71% | 20,14 | 53,34 |
| NONE | 16,10% | 60,81% | 5,67 | 15,80 |
| PORT_CONGESTION | 14,14% | 74,95% | 11,72 | 31,90 |
| LATE_BOARDING | 10,30% | 85,25% | 10,19 | 26,84 |

### 11.2 Insight principal

Las causas **WEATHER** y **TECHNICAL** explican conjuntamente el **44,71%** del retraso total. Al añadir **PORT_CONGESTION**, se alcanza aproximadamente el **74,95%** del retraso agregado.

Esto permite priorizar acciones sobre pocas palancas con alto impacto potencial.

---

## 12. Interacción clima–causa

El análisis muestra que el clima severo amplifica las disrupciones operativas.

En condiciones **ROUGH**:

- `TECHNICAL` alcanza un retraso medio aproximado de 27,6 min.
- `WEATHER` alcanza un retraso medio aproximado de 25,0 min.
- El P95 supera los 65 min.

En condiciones **STORM**:

- `TECHNICAL` alcanza un retraso medio aproximado de 42,6 min.
- `WEATHER` alcanza un retraso medio aproximado de 40,4 min.
- El P95 puede superar los 85–100 min.

### Interpretación

El mal clima no solo genera retrasos por sí mismo, sino que incrementa el impacto de otras incidencias. Por tanto, la gestión preventiva por umbrales meteorológicos es una palanca crítica.

---

## 13. Hotspots operativos

El análisis ruta × hora permite detectar combinaciones con retraso sistemático.

Se observan hotspots en rutas como:

- **BCN–IBZ**,
- **VAL–IBZ**,
- **VAL–PMI**.

Las franjas problemáticas se concentran especialmente entre:

```text
09:00–11:00
14:00–21:00
```

En estos hotspots, el OTR ≤ 15 min cae aproximadamente al rango **52–64%**, indicando una pérdida clara de fiabilidad operativa en ventanas concretas.

---

## 14. Semáforo operativo de rutas

El proyecto genera una lógica de semáforo para priorizar rutas según puntualidad y retrasos extremos.

| Ruta | OTR ≤ 15 min | Delay medio | P95 delay | Margen medio | Estado |
|---|---:|---:|---:|---:|---|
| BCN–IBZ | 65,52% | 15,18 | 44,30 | 25.818 | Prioridad |
| VAL–IBZ | 64,97% | 15,02 | 44,75 | 25.981 | Prioridad |
| VAL–PMI | 64,22% | 14,84 | 42,88 | 24.006 | Prioridad |
| BCN–PMI | 66,23% | 14,41 | 40,14 | 23.683 | Prioridad |

### Rutas saludables

Las rutas **DEN–FOR** y **DEN–IBZ** se identifican como rutas más saludables, con mejor puntualidad relativa y menor presión operativa.

---

## 15. Escenarios de impacto

El proyecto estima el impacto potencial de reducir determinadas causas de retraso.

| Escenario | Ahorro estimado |
|---|---:|
| Reducir WEATHER 10% | 2,84% del retraso total |
| Reducir TECHNICAL 10% | 1,63% del retraso total |
| Reducir PORT_CONGESTION 10% | 1,41% del retraso total |
| Reducir WEATHER 10% + TECHNICAL 10% | 4,47% del retraso total |

### Interpretación

La combinación de acciones sobre **WEATHER** y **TECHNICAL** ofrece el mayor impacto estimado, con un ahorro aproximado de **6.249,5 minutos** de retraso agregado.

---

## 16. Dashboard HTML interactivo

El dashboard está desarrollado en HTML con **Plotly.js** y está publicado en GitHub Pages.

[**Abrir dashboard Control Operativo Ferries**](https://amlacasta.github.io/control-operativo-eficiencia/dashboard/dashboard_control_operativo_ferries.html)

Funcionalidades principales:

- carga manual de CSV,
- filtros por ruta,
- filtros por clima,
- filtros por causa de disrupción,
- filtros por rango de fechas,
- selector de umbral OTR,
- KPIs principales,
- delay medio por ruta,
- Pareto de causas,
- evolución diaria de delay y OTR,
- semáforo operativo de rutas,
- interacción clima × causa,
- heatmap ruta × hora,
- top hotspots operativos,
- exportación del CSV filtrado.

El dashboard permite convertir el análisis del notebook en una herramienta exploratoria de lectura ejecutiva.

---

## 17. Recomendaciones operativas

### 17.1 Plan de contingencia por meteorología

Definir umbrales operativos para escenarios `WINDY`, `ROUGH` y `STORM`, con acciones como:

- buffer adicional,
- ajuste de slot,
- refuerzo de personal de embarque,
- comunicación preventiva al cliente,
- revisión de ventanas críticas.

Justificación: **WEATHER** es la principal fuente de retraso agregado.

### 17.2 Fiabilidad técnica

Reforzar mantenimiento preventivo y checks pre-salida en rutas con peor desempeño, especialmente cuando se esperan condiciones `ROUGH` o `STORM`.

Justificación: **TECHNICAL** tiene alto impacto y se amplifica con mal clima.

### 17.3 Gestión de congestión portuaria

Ajustar buffers y ventanas de atraque en franjas problemáticas.

Acciones posibles:

- coordinación con autoridad portuaria,
- revisión de turnos,
- mejora de procesos de embarque,
- priorización de ventanas críticas.

### 17.4 Control Tower semanal

Revisar semanalmente:

- OTR ≤ 15 min,
- delay medio,
- P95 delay,
- causas de disrupción,
- rutas AMBER,
- hotspots ruta × hora.

---

## 18. Outputs del proyecto

| Output | Descripción |
|---|---|
| `reports/executive_summary.md` | Resumen ejecutivo del análisis |
| `reports/figures/pareto_delay.png` | Pareto de causas de retraso |
| `reports/figures/heatmap_route_hour_delay.png` | Heatmap ruta × hora |
| `reports/figures/boxplot_delay_by_weather.png` | Distribución de retrasos por clima |
| `dashboard/dashboard_control_operativo_ferries.html` | Dashboard interactivo HTML |
| `reports/*.csv` | Tablas de KPIs, rutas, hotspots y semáforo |

---

## 19. Cómo reproducir el proyecto

### 19.1 Requisitos

Dependencias principales:

```text
pandas
numpy
matplotlib
seaborn
scikit-learn
```

### 19.2 Orden de ejecución

Ejecutar los notebooks en este orden:

```text
01_generate_dataset.ipynb
02_profiling_kpis.ipynb
03_diagnostics.ipynb
```

### 19.3 Flujo recomendado en Google Colab

1. Abrir `notebooks/01_generate_dataset.ipynb` y ejecutarlo.
2. Generar el dataset raw sintético.
3. Ejecutar `notebooks/02_profiling_kpis.ipynb`.
4. Revisar KPIs globales, rankings y semáforo.
5. Ejecutar `notebooks/03_diagnostics.ipynb`.
6. Revisar Pareto, hotspots, figuras y recomendaciones.
7. Abrir el dashboard HTML y cargar el CSV operativo generado.

---

## 20. Impacto de negocio

Este proyecto ayuda a convertir datos operativos en decisiones accionables.

### Puntualidad

Permite medir la fiabilidad real de la operación y distinguir entre una lectura estricta y una lectura operativa más realista.

### Priorización

Permite identificar rutas donde actuar primero, evitando decisiones basadas solo en intuición.

### Eficiencia operativa

Permite detectar causas que concentran retrasos y simular el impacto de reducirlas.

### Experiencia de cliente

Permite anticipar ventanas críticas y mejorar comunicación en situaciones de riesgo.

### Control de gestión

Permite conectar operación, ocupación y margen para tomar decisiones con visión de negocio.

---

## 21. Limitaciones

El proyecto utiliza datos sintéticos, por lo que sus resultados no deben interpretarse como resultados reales de ninguna compañía.

Limitaciones principales:

- dataset generado artificialmente,
- meteorología simulada,
- causas de disrupción simuladas,
- ingresos y costes sintéticos,
- no se incluyen datos reales de puertos,
- no se incluyen datos reales de flota,
- no se incluyen restricciones reales de atraque,
- no se incluye forecast futuro de demanda.

---

## 22. Próximos pasos

El sistema podría evolucionar incorporando:

- datos reales de operación,
- meteorología real,
- capacidad real de buques,
- tiempos reales de embarque y desembarque,
- restricciones portuarias,
- predicción de retrasos,
- simulador What-If operativo,
- dashboard interactivo tipo Streamlit o Power BI,
- alertas automáticas por ruta,
- integración con forecasting de demanda.

---

## 23. Conclusión

Este proyecto muestra un flujo completo de analítica aplicada a operaciones de transporte marítimo:

```text
datos → KPIs → diagnóstico → hotspots → semáforo → recomendaciones → dashboard
```

El valor principal no está únicamente en calcular indicadores, sino en convertirlos en una lógica de priorización operativa.

La solución permite identificar qué rutas requieren atención, qué causas explican mayor retraso y qué acciones pueden generar mayor impacto.

Este proyecto constituye la base operativa sobre la que pueden construirse soluciones más avanzadas de forecasting, pricing y optimización de recursos.
