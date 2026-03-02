# Executive Summary — Control Operativo y Eficiencia (Ferries)
## KPIs globales
- Servicios totales: **12000**
- Servicios completados: **11814**
- Cancel Rate: **1.55%**
- Delay medio: **11.83 min** | P95: **36.14 min**
- Ocupación media: **0.577**
- Margen medio: **27141.46** | Margen total: **320649262.45**

## Puntualidad (sensibilidad del umbral)
- OTR ≤ 5 min: 33.16%
- OTR ≤ 15 min: 73.93%

## Top rutas por retraso medio
| route_id   |   avg_delay_min |   p95_delay_min |   on_time_rate_% |   avg_margin |
|:-----------|----------------:|----------------:|-----------------:|-------------:|
| BCN-IBZ    |           15.18 |           44.3  |            23.32 |      25818.5 |
| VAL-IBZ    |           15.02 |           44.75 |            22.96 |      25981.5 |
| VAL-PMI    |           14.84 |           42.88 |            24.81 |      24006.1 |
| BCN-PMI    |           14.41 |           40.14 |            24.03 |      23682.8 |
| DEN-PMI    |           12.15 |           34.56 |            29.96 |      28622.4 |

## Pareto de causas (retraso total)
| disruption_reason   |   share_% |   cum_share_% |   avg_delay_min |   p95_delay_min |
|:--------------------|----------:|--------------:|----------------:|----------------:|
| WEATHER             |     28.44 |         28.44 |        18.2864  |           49.9  |
| TECHNICAL           |     16.27 |         44.71 |        20.1416  |           53.34 |
| NONE                |     16.1  |         60.81 |         5.67388 |           15.8  |
| PORT_CONGESTION     |     14.14 |         74.95 |        11.7202  |           31.9  |
| LATE_BOARDING       |     10.3  |         85.25 |        10.1887  |           26.84 |

## Semáforo de rutas (OTR≤15 + P95)
| route_id   |   on_time_15_% |   avg_delay |   p95_delay |   avg_margin |
|:-----------|---------------:|------------:|------------:|-------------:|
| BCN-IBZ    |          65.52 |       15.18 |       44.3  |      25818.5 |
| VAL-IBZ    |          64.97 |       15.02 |       44.75 |      25981.5 |
| VAL-PMI    |          64.22 |       14.84 |       42.88 |      24006.1 |
| BCN-PMI    |          66.23 |       14.41 |       40.14 |      23682.8 |

## Impacto estimado (escenarios)
- Reduce WEATHER 10% + TECHNICAL 10%: ahorro ~4.47% (6249.5 min)
- Reduce WEATHER 10%: ahorro ~2.84% (3975.5 min)
- Reduce TECHNICAL 10%: ahorro ~1.63% (2274.0 min)
- Reduce PORT_CONGESTION 10%: ahorro ~1.41% (1976.0 min)

## Figuras
- `reports/figures/pareto_delay.png`
- `reports/figures/heatmap_route_hour_delay.png`
- `reports/figures/boxplot_delay_by_weather.png`
