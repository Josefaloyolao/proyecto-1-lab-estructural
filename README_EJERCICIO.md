# Ejercicio — Análisis Elástico 2D con OpenSeesPy

## Objetivo

Construir y resolver un modelo bidimensional elástico lineal mediante OpenSeesPy. Obtener reacciones, desplazamientos y fuerzas locales de extremo (axial, corte y momento) de todos los elementos.

## Geometría

El sistema está en el plano global X–Y:

```
         (0,5)
           |
           |  columna superior (3 m)
           |
  (0,2)----+--------(5,2)--------(8,2)
  unión    |  viga 1 (5 m)   viga 2 (3 m)
           |                    apoyo
  columna  |                    articulado
  inferior |
  (2 m)    |
           |
         (0,0)
         empotramiento
```

- **Columna vertical** de 5 m total: 2 m inferiores + 3 m superiores.
- **Viga horizontal** de 8 m: dividida en tramo de 5 m y tramo de 3 m.
- La columna y la viga comparten el nodo `(0,2)` con unión rígida.

## Apoyos

| Nodo | Tipo | Ux | Uy | Rz |
|------|------|----|----|-----|
| `(0,0)` | Empotramiento | 0 | 0 | 0 |
| `(8,2)` | Articulado fijo | 0 | 0 | libre |

El apoyo derecho se interpreta como **articulado**: impide traslaciones pero permite giro (sin reacción de momento).

## Cargas

| Carga | Magnitud | Dirección | Ubicación |
|-------|----------|-----------|-----------|
| Uniforme `q` | 17 kN/m | +X (horizontal) | Sobre los 5 m de columna |
| Puntual `P` | 20 kN | -Y (vertical) | Nodo `(5,2)` |

El peso propio no está incluido.

## Propiedades de sección

### Columna — IPE 400 (acero ASTM A36)

| Parámetro | Valor | Unidad |
|-----------|-------|--------|
| E | 200 | GPa |
| Fy | 250 | MPa |
| A | 84.46 | cm² |
| Ix | 23130 | cm⁴ |
| Wx | 1156 | cm³ |

### Viga — Rectangular 40×40 cm (hormigón elástico)

| Parámetro | Valor | Unidad |
|-----------|-------|--------|
| E | 25 | GPa |
| A | 0.160 | m² |
| I | 0.002133 | m⁴ |

## Modelo numérico

- Modelo 2D, 3 GDL por nodo: `Ux`, `Uy`, `Rz`.
- Elementos `elasticBeamColumn`.
- Transformación geométrica `Linear`.
- Análisis estático lineal de primer orden.
- Unidades: **N, m, Pa**.

## Resultados obtenidos

### Reacciones

| Apoyo | Rx (kN) | Ry (kN) | M (kN·m) |
|-------|---------|---------|----------|
| Base `(0,0)` | 36.123 | 8.200 | -24.146 |
| Derecho `(8,2)` | -121.123 | 11.800 | 0.000 |

### Equilibrio global

| Verificación | Residuo |
|-------------|---------|
| ΣFx | ≈ 0 |
| ΣFy | ≈ 0 |
| ΣM_base | ≈ 0 |

Los residuos son del orden de 10⁻¹⁰, es decir, precisión de máquina.

### Fuerzas locales de extremo [kN, kN·m]

| Elemento | Ni | Vi | Mi | Nj | Vj | Mj |
|----------|-----|-----|------|-----|-----|------|
| Columna inferior | 8.200 | -36.123 | -24.146 | -8.200 | 70.123 | -82.101 |
| Columna superior | 0.000 | 51.000 | 76.500 | -0.000 | 0.000 | -0.000 |
| Viga 0–5 m | 121.123 | 8.200 | 5.601 | -121.123 | -8.200 | 35.400 |
| Viga 5–8 m | 121.123 | -11.800 | -35.400 | -121.123 | 11.800 | 0.000 |

### Esfuerzo elástico de la columna (N/A + M/W)

La sección crítica de la columna alcanza un esfuerzo elástico de referencia (no reemplaza verificación normativa completa).

## Ejecución

```bash
cd "proyecto 1"
.\.venv\Scripts\activate
python src\opensees\modelo_definitivo_opensees.py
```

## Archivos generados

- `resultados_definitivos.json` — Todos los resultados en JSON.
- `fuerzas_elementos_definitivas.csv` — Fuerzas locales en CSV.
