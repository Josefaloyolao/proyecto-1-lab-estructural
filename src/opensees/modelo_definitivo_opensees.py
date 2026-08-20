"""
Analisis definitivo del ejercicio mediante OpenSeesPy.

UNIDADES: N, m, Pa.

MODELO:
  * Columna vertical de 5 m: 2 m bajo la union y 3 m sobre ella.
  * Base de columna empotrada: Ux=Uy=Rz=0.
  * Viga horizontal de 8 m unida rigidamente a la columna en y=2 m.
  * Apoyo derecho FIJO ARTICULADO: Ux=0, Uy=0 y Rz libre.
  * Carga uniforme horizontal q=17 kN/m en los 5 m de columna.
  * Carga puntual P=20 kN hacia abajo a 5 m de la columna.
  * Peso propio no incluido.

SALIDAS:
  * Reacciones Rx, Ry y M de los apoyos.
  * Desplazamientos Ux, Uy y Rz de todos los nodos.
  * Axial, corte y momento local en ambos extremos de cada elemento.
  * JSON y CSV con todos los resultados.

EJECUCION:
  python modelo_definitivo_opensees.py
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

try:
    import openseespy.opensees as ops
except ModuleNotFoundError as exc:
    raise SystemExit(
        "Falta OpenSeesPy. Instale con: python -m pip install openseespy"
    ) from exc


# ---------------------------------------------------------------------------
# Propiedades y cargas
# ---------------------------------------------------------------------------
E_ACERO = 200.0e9          # Pa
FY_ACERO = 250.0e6         # Pa, ASTM A36

# Columna seleccionada: IPE 400, eje fuerte.
A_COLUMNA = 84.46e-4       # m2
I_COLUMNA = 23130.0e-8     # m4
W_COLUMNA = 1156.0e-6      # m3

# Viga rectangular 40 x 40 cm, hormigon elastico no fisurado adoptado.
E_VIGA = 25.0e9            # Pa
B_VIGA = 0.40              # m
H_VIGA = 0.40              # m
A_VIGA = B_VIGA * H_VIGA
I_VIGA = B_VIGA * H_VIGA**3 / 12.0

Q = 17.0e3                 # N/m, horizontal hacia +X
P = 20.0e3                 # N, vertical hacia -Y


def construir_y_analizar() -> dict:
    ops.wipe()
    ops.model("basic", "-ndm", 2, "-ndf", 3)

    coordenadas = {
        1: (0.0, 0.0),     # base empotrada
        2: (0.0, 2.0),     # union rigida columna-viga
        3: (0.0, 5.0),     # extremo libre superior
        4: (5.0, 2.0),     # nodo de la carga puntual
        5: (8.0, 2.0),     # apoyo derecho
    }
    for nodo, (x, y) in coordenadas.items():
        ops.node(nodo, x, y)

    # Restricciones [Ux, Uy, Rz].
    ops.fix(1, 1, 1, 1)    # empotramiento
    ops.fix(5, 1, 1, 0)    # apoyo fijo articulado

    ops.geomTransf("Linear", 1)

    elementos = {
        1: {"nombre": "columna_inferior", "i": 1, "j": 2},
        2: {"nombre": "columna_superior", "i": 2, "j": 3},
        3: {"nombre": "viga_0_a_5m", "i": 2, "j": 4},
        4: {"nombre": "viga_5_a_8m", "i": 4, "j": 5},
    }

    ops.element("elasticBeamColumn", 1, 1, 2, A_COLUMNA, E_ACERO, I_COLUMNA, 1)
    ops.element("elasticBeamColumn", 2, 2, 3, A_COLUMNA, E_ACERO, I_COLUMNA, 1)
    ops.element("elasticBeamColumn", 3, 2, 4, A_VIGA, E_VIGA, I_VIGA, 1)
    ops.element("elasticBeamColumn", 4, 4, 5, A_VIGA, E_VIGA, I_VIGA, 1)

    # Patron de carga.
    ops.timeSeries("Linear", 1)
    ops.pattern("Plain", 1, 1)

    # Para un elemento vertical i->j, -local-y corresponde a global +X.
    ops.eleLoad("-ele", 1, "-type", "-beamUniform", -Q)
    ops.eleLoad("-ele", 2, "-type", "-beamUniform", -Q)
    ops.load(4, 0.0, -P, 0.0)

    # Analisis.
    ops.system("BandGeneral")
    ops.numberer("Plain")
    ops.constraints("Plain")
    ops.integrator("LoadControl", 1.0)
    ops.algorithm("Linear")
    ops.analysis("Static")

    codigo = ops.analyze(1)
    if codigo != 0:
        raise RuntimeError(f"OpenSees no completo el analisis; codigo={codigo}")

    ops.reactions()
    reacciones = {
        "base_nodo_1": list(ops.nodeReaction(1)),
        "apoyo_derecho_nodo_5": list(ops.nodeReaction(5)),
    }

    desplazamientos = {
        str(n): {
            "coordenadas_m": list(coordenadas[n]),
            "Ux_m": ops.nodeDisp(n, 1),
            "Uy_m": ops.nodeDisp(n, 2),
            "Rz_rad": ops.nodeDisp(n, 3),
        }
        for n in coordenadas
    }

    fuerzas = {}
    for e, datos in elementos.items():
        f = list(ops.eleResponse(e, "localForce"))
        fuerzas[str(e)] = {
            **datos,
            "Ni_N": f[0],
            "Vi_N": f[1],
            "Mi_Nm": f[2],
            "Nj_N": f[3],
            "Vj_N": f[4],
            "Mj_Nm": f[5],
        }

    columna = [fuerzas["1"], fuerzas["2"]]
    viga = [fuerzas["3"], fuerzas["4"]]

    def maximo(grupo: list[dict], claves: tuple[str, str]) -> float:
        return max(abs(e[clave]) for e in grupo for clave in claves)

    resumen = {
        "columna_N_max_N": maximo(columna, ("Ni_N", "Nj_N")),
        "columna_V_max_N": maximo(columna, ("Vi_N", "Vj_N")),
        "columna_M_max_Nm": maximo(columna, ("Mi_Nm", "Mj_Nm")),
        "viga_N_max_N": maximo(viga, ("Ni_N", "Nj_N")),
        "viga_V_max_N": maximo(viga, ("Vi_N", "Vj_N")),
        "viga_M_max_Nm": maximo(viga, ("Mi_Nm", "Mj_Nm")),
    }

    # Seccion critica elastica N/A + M/W.
    candidatos = []
    for e in columna:
        candidatos.extend(
            [
                {"elemento": e["nombre"], "extremo": "i", "N_N": abs(e["Ni_N"]), "M_Nm": abs(e["Mi_Nm"])},
                {"elemento": e["nombre"], "extremo": "j", "N_N": abs(e["Nj_N"]), "M_Nm": abs(e["Mj_Nm"])},
            ]
        )
    critica = max(candidatos, key=lambda s: s["N_N"] / A_COLUMNA + s["M_Nm"] / W_COLUMNA)
    sigma = critica["N_N"] / A_COLUMNA + critica["M_Nm"] / W_COLUMNA
    critica.update({"sigma_elastica_Pa": sigma, "Fy_Pa": FY_ACERO, "relacion_sigma_Fy": sigma / FY_ACERO})

    # Equilibrio global.
    rb = reacciones["base_nodo_1"]
    rd = reacciones["apoyo_derecho_nodo_5"]
    equilibrio = {
        "suma_Fx_N": rb[0] + rd[0] + Q * 5.0,
        "suma_Fy_N": rb[1] + rd[1] - P,
        "suma_M_base_Nm": rb[2] + 8.0 * rd[1] - 2.0 * rd[0] + rd[2] - (Q * 5.0) * 2.5 - P * 5.0,
    }

    return {
        "unidades": {"fuerza": "N", "longitud": "m", "momento": "N.m"},
        "modelo": {
            "base": "Ux=Uy=Rz=0",
            "union_columna_viga": "rigida",
            "apoyo_derecho": "fijo articulado: Ux=0, Uy=0, Rz libre",
            "peso_propio": "no incluido",
        },
        "reacciones": reacciones,
        "desplazamientos": desplazamientos,
        "fuerzas_locales_elementos": fuerzas,
        "maximos_absolutos": resumen,
        "seccion_critica_columna": critica,
        "residuos_equilibrio": equilibrio,
    }


def guardar(resultados: dict) -> tuple[Path, Path]:
    carpeta = Path(__file__).resolve().parent
    ruta_json = carpeta / "resultados_definitivos.json"
    ruta_csv = carpeta / "fuerzas_elementos_definitivas.csv"

    ruta_json.write_text(json.dumps(resultados, indent=2, ensure_ascii=False), encoding="utf-8")

    with ruta_csv.open("w", newline="", encoding="utf-8") as archivo:
        campos = ["elemento", "nombre", "nodo_i", "nodo_j", "Ni_kN", "Vi_kN", "Mi_kNm", "Nj_kN", "Vj_kN", "Mj_kNm"]
        escritor = csv.DictWriter(archivo, fieldnames=campos)
        escritor.writeheader()
        for numero, e in resultados["fuerzas_locales_elementos"].items():
            escritor.writerow({
                "elemento": numero,
                "nombre": e["nombre"],
                "nodo_i": e["i"],
                "nodo_j": e["j"],
                "Ni_kN": e["Ni_N"] / 1e3,
                "Vi_kN": e["Vi_N"] / 1e3,
                "Mi_kNm": e["Mi_Nm"] / 1e3,
                "Nj_kN": e["Nj_N"] / 1e3,
                "Vj_kN": e["Vj_N"] / 1e3,
                "Mj_kNm": e["Mj_Nm"] / 1e3,
            })
    return ruta_json, ruta_csv


def imprimir(resultados: dict) -> None:
    print("\n=== REACCIONES ===")
    for nombre, r in resultados["reacciones"].items():
        print(f"{nombre:28s} Rx={r[0]/1e3:10.3f} kN  Ry={r[1]/1e3:10.3f} kN  M={r[2]/1e3:10.3f} kN.m")

    print("\n=== AXIAL, CORTE Y MOMENTO LOCAL DE EXTREMO ===")
    print("Elemento                     Ni       Vi       Mi       Nj       Vj       Mj")
    print("                           [kN]     [kN]   [kN.m]    [kN]     [kN]   [kN.m]")
    for e in resultados["fuerzas_locales_elementos"].values():
        print(
            f"{e['nombre']:25s} "
            f"{e['Ni_N']/1e3:8.3f} {e['Vi_N']/1e3:8.3f} {e['Mi_Nm']/1e3:8.3f} "
            f"{e['Nj_N']/1e3:8.3f} {e['Vj_N']/1e3:8.3f} {e['Mj_Nm']/1e3:8.3f}"
        )

    print("\n=== MAXIMOS ABSOLUTOS ===")
    m = resultados["maximos_absolutos"]
    print(f"Columna: N={m['columna_N_max_N']/1e3:.3f} kN, V={m['columna_V_max_N']/1e3:.3f} kN, M={m['columna_M_max_Nm']/1e3:.3f} kN.m")
    print(f"Viga:    N={m['viga_N_max_N']/1e3:.3f} kN, V={m['viga_V_max_N']/1e3:.3f} kN, M={m['viga_M_max_Nm']/1e3:.3f} kN.m")
    print("Residuos de equilibrio:", resultados["residuos_equilibrio"])


def main() -> None:
    resultados = construir_y_analizar()
    json_path, csv_path = guardar(resultados)
    imprimir(resultados)
    print(f"\nJSON: {json_path}")
    print(f"CSV:  {csv_path}")


if __name__ == "__main__":
    main()
