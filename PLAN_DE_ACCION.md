# Plan de Acción — Laboratorio Estructural Digital

## Visión General

Construir un modelo estructural 3D lineal elástico del Edificio de Ingeniería en OpenSeesPy, exportar resultados a Unity para visualización/interacción, y agregar AR en el edificio real. Separado del modelo global: secciones de fibra RC (M-φ y P-M).

---

## SEMANA 0 (19–21 ago) — Intro + Primeros pasos OpenSees

### Objetivo
Modelo 2D mínimo funcional en OpenSees.

### Tareas
| # | Tarea | Responsable | Criterio de aceptación |
|---|-------|-------------|------------------------|
| 0.1 | Instalar OpenSeesPy, verificar versión | Todos | `import openseespy.opensees as ops; print(ops.version())` funciona |
| 0.2 | Modelo 2D viga-columna: 2 nodos, 1 elemento, apoyo, carga | Todos | Resultados numéricos verificables a mano |
| 0.3 | Calcular reacciones y deformadas | Todos | Reacciones equilibran carga aplicada |
| 0.4 | Familiarizarse con Unity (instalar, escena vacía) | Unity team | Escena vacía corriendo en手机/PC |

### Entrega LAB 0 (jue 20 ago, 5 pts)
- Script OpenSeesPy con modelo 2D completo
- Reacciones y diagramas básicos

---

## SEMANA 1 (24–28 ago) — Benchmark 3D + Verificación

### Objetivo
Benchmark 3D con 6 GDL/nodo, ejes locales, apoyos, cargas, reacciones y fuerzas internas.

### Tareas
| # | Tarea | Responsable | Criterio de aceptación |
|---|-------|-------------|------------------------|
| 1.1 | Definir geometría 3D del edificio (nodos, elementos) | Estructural | JSON `geometry.json` con todos los nodos y elementos |
| 1.2 | Asignar propiedades de material (E, A, I, G) | Estructural | Propiedades coherentes con dimensiones |
| 1.3 | Definir apoyos y restricciones (6 GDL) | Estructural | Apoyos correctos en base, verificación visual |
| 1.4 | Implementar diafragmas rígidos | Estructural | `rigidDiaphragm` activo en cada piso |
| 1.5 | Definir ejes locales (geomTransf) | Estral | Orientación verificable visualmente |
| 1.6 | Carga lateral idealizada EX y EY | Estructural | Patrón lateral parametrizable |
| 1.7 | Carga gravitacional G (peso propio simplificado) | Estructural | Reacciones = carga total |
| 1.8 | Exportar geometría a JSON para Unity | Estructural | Contrato JSON definido |
| 1.9 | Leer JSON en Unity, crear GameObjects | Unity | Geometría visible en Unity con IDs |
| 1.10 | Verificar equilibrio global | Todos | ΣF + ΣR < 1e-6 |
| 1.11 | Verificar superposición (G+EX = G + EX) | Todos | Numéricamente exacto |

### Entrega LAB 1 (jue 27 ago, 10 pts)
- Benchmark 3D funcional
- Verificación de GDL, ejes, apoyos, cargas, reacciones, fuerzas internas

### Entrega grande (vie 28 ago, 20 pts)
- Verificación cuantitativa del benchmark
- Arquitectura inicial del repo
- Contrato JSON definido

---

## SEMANA 2 (31 ago–4 sep) — Edificio Completo + Gravedad + Áreas Tributarias + Unity

### Objetivo
Modelo global completo, carga de losa + terminaciones por áreas tributarias, primer viewer 3D.

### Tareas
| # | Tarea | Responsable | Criterio de aceptación |
|---|-------|-------------|------------------------|
| 2.1 | Completar geometría de todos los pisos | Estructural | Todos los nodos y elementos del edificio |
| 2.2 | Definir cargas superficiales q_G (losa + terminaciones) | Estructural | Valor documentado con unidades |
| 2.3 | Implementar cálculo de áreas tributarias | Tributary | Script que calcula A_trib por viga |
| 2.4 | Transferir cargas de losa → vigas via áreas tributarias | Tributary | Σ(cargas transferidas) = q·A_total |
| 2.5 | Aplicar cargas de viga como nodales o distribuidas | Estructural | Cargas correctas en elementos |
| 2.6 | Peso propio de vigas, columnas, muros | Estructural | Según convención del profesor |
| 2.7 | Ejecutar caso G, obtener resultados | Estructural | Deformada, reacciones, diagramas |
| 2.8 | Exportar resultados G a JSON | Estructural | Contrato de resultados definido |
| 2.9 | Importar modelo + cargas + resultados en Unity | Unity | Todo visible y navegable |
| 2.10 | Visualizar áreas tributarias en Unity | Unity | Polígonos visibles por piso |
| 2.11 | QA: conservación de carga verificada | Todos | Error < 1e-10 |
| 2.12 | Detectar errores de conectividad en Unity | Unity | Nodos sin elemento conectado visibles |

### Entrega LAB 2 (jue 3 sep, 10 pts)
- Geometría estructural completa
- Primeros chequeos y viewer 3D

### Entrega grande (vie 4 sep, 20 pts)
- Modelo global completo
- Carga de losa + terminaciones con áreas tributarias
- Conservación de carga verificada
- QA en Unity

---

## SEMANA 3 (7–11 sep) — Carga Viva + Sismo + Superposición + Capacidad RC

### Objetivo
Casos Q, EX, EY completos. Superposición verificada. Fiber sections y curvas P-M.

### Tareas
| # | Tarea | Responsable | Criterio de aceptación |
|---|-------|-------------|------------------------|
| 3.1 | Definir carga viva q_Q (valor, distribución) | Estral | Carga superficial uniforme |
| 3.2 | Aplicar q_Q via áreas tributarias | Tributary | Conservación de carga |
| 3.3 | Ejecutar caso Q | Estructural | Resultados consistentes |
| 3.4 | Refinar patrón lateral EX, EY | Estral | Patrón verificable |
| 3.5 | Ejecutar EX y EY independientes | Estructural | Resultados asimétricos correctos |
| 3.6 | Demostrar superposición: R(G+Q+EX) = R(G)+R(Q)+R(EX) | Todos | Numéricamente exacto |
| 3.7 | Construir Fiber Section de columna RC | RC | Section con concreto + acero |
| 3.8 | Obtener curva M-φ para sección representativa | RC | CurvaPhysicalmente interpretable |
| 3.9 | Comparar M-φ con curso de hormigón armado | RC | Al menos 1 comparación independiente |
| 3.10 | Generar curva P-M para columna | RC | P-M completo |
| 3.11 | Generar curva P-M para muro | RC | P-M completo |
| 3.12 | Exportar curvas P-M a JSON | RC | Contrato definido |
| 3.13 | Superponer demanda del modelo global sobre curva P-M | RC+Est | Punto de demanda visible |
| 3.14 | Cargar curvas P-M en Unity | Unity | Visualización interactiva |

### Entrega LAB 3 (jue 10 sep, 10 pts)
- G, Q, EX, EY funcionando
- Superposición inicial
- Fiber Section y M-φ

### Entrega grande (vie 11 sep, 20 pts)
- Superposición verificada
- Curvas P-M de columna y muro
- Primera demanda/capacidad

---

## SEMANA 4 (14–18 sep) — Integración Completa en Unity

### Objetivo
Todos los resultados disponibles en Unity. Contrato OpenSees↔Unity verificado.

### Tareas
| # | Tarea | Responsable | Criterio de aceptación |
|---|-------|-------------|------------------------|
| 4.1 | Selección de elementos en Unity (click) | Unity | elementTag accesible |
| 4.2 | Mostrar apoyos, restricciones, ejes locales | Unity | Toggle on/off |
| 4.3 | Mostrar cargas aplicadas (flechas) | Unity | Escala correcta |
| 4.4 | Visualizar deformada | Unity | Escala configurable |
| 4.5 | Diagramas de esfuerzos (M, V, N) | Unity | Por elemento seleccionado |
| 4.6 | P-M junto a elemento seleccionado | Unity | Demanda vs capacidad |
| 4.7 | Verificar contrato OpenSees↔Unity | Todos | Todo elementTag existe 1 vez |
| 4.8 | QA completo de resultados | Todos | Todos los casos verificados |

### Entrega LAB 4 (jue 17 sep, 10 pts)
- Selección, apoyos, cargas, áreas tributarias, deformada, diagramas, P-M

### Entrega grande (vie 18 sep, 20 pts)
- Contrato OpenSees↔Unity verificado
- QA completo
- Diagramas y demanda-capacidad funcionales

---

## SEMANA 5 (21–25 sep) — Interactividad + Modificación del Modelo

### Objetivo
Interfaz interactiva. Modificación de parámetros. Sidequests.

### Tareas
| # | Tarea | Responsable | Criterio de aceptación |
|---|-------|-------------|------------------------|
| 5.1 | Sliders para combinaciones de carga (λ) | Unity | Superposición instantánea |
| 5.2 | Cambios que NO requieren reanálisis | Unity | Solo recombinar resultados existentes |
| 5.3 | Identificar qué SÍ requiere reanálisis | Todos | Documentado |
| 5.4 | SQ1: Tributary Area Inspector | Tributary | Seleccionar viga, definir polígono, calcular carga |
| 5.5 | SQ2: Load Combination Explorer | Unity | Modificar λ, ver deformada/diagramas |
| 5.6 | SQ3: Section Capacity Explorer | RC | Ver M-φ, P-M, punto demanda |
| 5.7 | SQ4: Carga móvil del usuario | Todos | Regla de transferencia definida y documentada |
| 5.8 | Modificar al menos 2 familias de parámetros | Unity | Sliders funcionales |
| 5.9 | Preparar build para móvil | Unity | APK o build funcional |

### Entrega LAB 5 (jue 24 sep, 10 pts)
- Sliders, superposición instantánea, modificación de parámetros

### Entrega grande (vie 25 sep, 20 pts)
- Laboratorio estructural interactivo v1
- Sidequests integrados
- Preparación móvil

---

## SEMANA 6 (28 sep–2 oct) — AR Básica

### Objetivo
AR funcional en el edificio real. Marker → pose → anchor → elemento + resultado.

### Tareas
| # | Tarea | Responsable | Criterio de aceptación |
|---|-------|-------------|------------------------|
| 6.1 | Configurar AR Foundation en Unity | AR | Proyecto compila para Android/iOS |
| 6.2 | Implementar image tracking con marker | AR | Marker detectado, pose estable |
| 6.3 | Crear anchor sobre elemento real | AR | Elemento alineado con edificio |
| 6.4 | Transformar coordenadas OpenSees → Unity → AR | AR | Escala y posición correctas |
| 6.5 | Mostrar resultado OpenSees sobre elemento AR | AR | Deformada o diagrama visible |
| 6.6 | Cuantificar error de registro | AR | Error medido y documentado |
| 6.7 | Validar en el edificio real | Todos | Funciona in situ |

### Entrega LAB 6 (jue 1 oct, 10 pts)
- Marker → pose → anchor → elemento real + resultado OpenSees

### Entrega grande (vie 2 oct, 20 pts)
- Validación AR completa
- Transformación de coordenadas verificada
- Error de registro documentado
- QA global

---

## SEMANA 7 (5–9 oct) — Integración Final + Honors Track

### Objetivo
Demo final completa. Honors track para bonificación.

### Tareas Obligatorias
| # | Tarea | Responsable |
|---|-------|-------------|
| 7.1 | Demo final completa | Todos |
| 7.2 | Defensa individual | Cada uno |
| 7.3 | Informe final | Todos |
| 7.4 | Release reproducible | Todos |
| 7.5 | Documentar limitaciones | Todos |
| 7.6 | Documentar uso de IA | Todos |

### Honors Track (opcional, +20 pts max)
| # | Objetivo | Pts |
|---|----------|-----|
| H1 | Google Cardboard VR | +4 |
| H2 | AR avanzada (múltiples markers, persistencia) | +4 |
| H3 | AR estructural (diagramas, deformada, P-M en AR) | +4 |
| H4 | Reanálisis OpenSees en vivo (cliente-servidor) | +4 |
| H5 | Capacidad/análisis avanzado (P-Mx-My, 2do orden) | +4 |

### Entrega (jue 8 oct, 70 pts)
- Demo final + defensa individual + Honors

### Entrega (vie 9 oct, 20 pts)
- Informe final + release + documentación

---

## Convención de Commits

Formato: `[WkX] Descripción corta`

Ejemplos:
- `[Wk0] Add 2D OpenSees benchmark`
- `[Wk1] Define 3D geometry JSON schema`
- `[Wk2] Implement tributary area calculation`
- `[Wk3] Add fiber section P-M for column`
- `[WkSQ1] Add tributary area inspector UI`

---

## Roles Sugeridos (adaptar al grupo)

| Rol | Responsabilidades |
|-----|-------------------|
| **Estructural** | OpenSeesPy, modelo global, verificación, superposición |
| **Tributary** | Áreas tributarias, conservación de cargas, SQ1, SQ4 |
| **RC** | Fiber sections, M-φ, P-M, demanda-capacidad |
| **Unity** | Visualización, interacción, UI, contratos JSON |
| **AR** | AR Foundation, image tracking, anchors, transformación coordenadas |

---

## Invariantes Físicos (verificar siempre)

1. **Equilibrio global**: ΣF_aplicadas + ΣR = 0
2. **Conservación de carga tributaria**: Σ(q·A_trib) = q·A_total
3. **Superposición lineal**: R(A+B) = R(A) + R(B)
4. **Unidades**: SI consistente en todo momento
5. **IDs**: Cada elementTag exportado existe exactamente 1 vez en viewer
