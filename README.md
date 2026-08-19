# Proyecto 1 — Laboratorio Estructural Digital

Laboratorio estructural digital 3D del Edificio de Ingeniería.

## Stack

- **OpenSeesPy** — Análisis estructural lineal elástico 3D y secciones de fibra RC.
- **Unity** — Visualización 3D, pre/postproceso, interacción, AR.
- **JSON** — Contrato de datos entre OpenSees y Unity.
- **AR Foundation** — Realidad aumentada en el edificio real.

## Estructura

```
proyecto-1-lab-estructural/
├── src/
│   ├── opensees/          # Scripts de análisis estructural
│   ├── unity/             # Proyecto Unity
│   └── ar/                # Componentes AR
├── data/
│   ├── geometry/          # Geometría estructural (JSON)
│   ├── loads/             # Cargas (JSON)
│   ├── results/           # Resultados OpenSees (JSON)
│   └── tributary_areas/   # Áreas tributarias (JSON)
├── tests/                 # Verificaciones y tests
├── docs/                  # Documentación
├── AGENTS.md
└── README.md
```

## Semanas

| Semana | Foco |
|--------|------|
| 0 | Intro + primeros pasos OpenSees |
| 1 | Benchmark 3D + verificación |
| 2 | Edificio completo + gravedad + Unity |
| 3 | Carga viva + sismo + superposición + capacidad RC |
| 4 | Integración resultados en Unity |
| 5 | Interactividad + modificación del modelo |
| 6 | AR básica |
| 7 | Integración final + Honors Track |
