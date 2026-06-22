#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Descomposición del crecimiento del salario real por hora en España, 1996-2021.

Fuente de datos:
  - EUKLEMS & INTANProd, release 2024 (LLEE), solo España:
        ES_growth accounts.xlsx, ES_national accounts.xlsx
  - IPC del INE (medias anuales) empalmado:
        269.xlsx    -> IPC base 1992 (1995-2001)
        76144.xlsx  -> IPC base 2025 (2002-2025)
    Enlace 2001->2002: inflación media supuesta del 3,5% (dato real INE 2002).

Identidad (nivel total economía, exacta):
    Δln(W/Pc) = Δln(s_L) + Δln(VA_Q/H) + [Δln(P_VA) - Δln(Pc)]
con  W = LAB/H (compensación laboral por hora), s_L = LAB/VA (participación del
trabajo), VA_Q/H productividad real por hora, P_VA = VA/VA_Q deflactor del VA,
Pc = IPC.

La productividad por hora Δln(VA_Q/H) se abre en:
    - cinco factores INTRASECTORIALES (within), media ponderada por horas de las
      contribuciones por industria de EUKLEMS:
        composición laboral, capital TIC, capital no-TIC, capital intangible, PTF
    - REASIGNACIÓN sectorial (between): residuo que reconcilia la productividad
      intrasectorial con la agregada (efecto de mover horas entre ramas).

Salidas: 2 PNG y 2 CSV en las rutas correctas relativas a la estructura del proyecto.
"""

import os
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

warnings.filterwarnings("ignore")

# Rutas dinámicas basadas en la ubicación del script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
GA = os.path.join(BASE_DIR, "..", "data", "ES_growth accounts.xlsx")
NA = os.path.join(BASE_DIR, "..", "data", "ES_national accounts.xlsx")
IPC_OLD_PATH = os.path.join(BASE_DIR, "..", "data", "269.xlsx")
IPC_NEW_PATH = os.path.join(BASE_DIR, "..", "data", "76144.xlsx")


OUT_IMG_DIR = os.path.join(BASE_DIR, "..", "imagenes")
os.makedirs(OUT_IMG_DIR, exist_ok=True)
OUT_DATA_DIR = os.path.join(BASE_DIR, "..")

YEARS = list(range(1995, 2022))           # cobertura EUKLEMS
DYEARS = list(range(1996, 2022))          # años con variación (deltas)
INFL_2002 = 0.035                          # enlace IPC 2001->2002

# ---------------------------------------------------------------------------
# 1. Utilidades de carga
# ---------------------------------------------------------------------------
def load_sheet(path, sheet):
    """Devuelve DataFrame indexado por código NACE con columnas = años (float)."""
    df = pd.read_excel(path, sheet_name=sheet).set_index("nace_r2_code")
    yrs = [c for c in df.columns if str(c).strip().isdigit()]
    out = df[yrs].apply(pd.to_numeric, errors="coerce")
    out.columns = [int(c) for c in out.columns]
    return out

# ---------------------------------------------------------------------------
# 2. IPC empalmado -> inflación anual (Δln Pc) 1996-2021
# ---------------------------------------------------------------------------
def read_ipc(path):
    raw = pd.read_excel(path, sheet_name=0, header=None)
    rows = {}
    for _, r in raw.iterrows():
        a, b = r[0], r[1]
        try:
            y = int(float(a))
        except (TypeError, ValueError):
            continue
        if 1900 < y < 2100 and pd.notna(b):
            rows[y] = float(b)
    return pd.Series(rows).sort_index()

ipc_old = read_ipc(IPC_OLD_PATH)     # base 1992, 1995-2001
ipc_new = read_ipc(IPC_NEW_PATH)     # base 2025, 2002-2025

dlnPc = {}
# 1996-2001: serie antigua
for y in range(1996, 2002):
    dlnPc[y] = np.log(ipc_old[y] / ipc_old[y - 1])
# 2002: enlace supuesto
dlnPc[2002] = np.log(1 + INFL_2002)
# 2003-2021: serie nueva
for y in range(2003, 2022):
    dlnPc[y] = np.log(ipc_new[y] / ipc_new[y - 1])
dlnPc = pd.Series(dlnPc)

# ---------------------------------------------------------------------------
# 3. Agregados (TOT) e identidad exacta
# ---------------------------------------------------------------------------
LAB = load_sheet(GA, "LAB")
VA  = load_sheet(GA, "VA_CP")
VAQ = load_sheet(GA, "VA_Q")
H   = load_sheet(NA, "H_EMP")

lab_t, va_t, vaq_t, h_t = LAB.loc["TOT"], VA.loc["TOT"], VAQ.loc["TOT"], H.loc["TOT"]

def dln(s, y):
    return np.log(s[y] / s[y - 1])

rows = []
for y in DYEARS:
    c_labshare = dln(lab_t / va_t, y)            # Δln participación del trabajo
    c_prod     = dln(vaq_t / h_t, y)             # Δln productividad real por hora
    c_pva      = dln(va_t / vaq_t, y)            # Δln deflactor del VA
    c_wedge    = c_pva - dlnPc[y]                # cuña de precios
    g_real     = dln(lab_t / h_t, y) - dlnPc[y]  # Δln salario real por hora
    rows.append(dict(year=y, c_labshare=c_labshare, c_prod=c_prod,
                     c_wedge=c_wedge, g_real=g_real))
agg = pd.DataFrame(rows).set_index("year")

# ---------------------------------------------------------------------------
# 4. Productividad: within (5 factores) + between (reasignación)
# ---------------------------------------------------------------------------
PART_MANUF = ["C10-C12", "C13-C15", "C16-C18", "C19", "C20", "C21",
              "C22-C23", "C24-C25", "C26", "C27", "C28", "C29-C30", "C31-C33"]
PART_SECT  = ["A", "B", "D", "E", "F", "G", "H", "I", "J", "K", "L",
              "M", "N", "O", "P", "Q", "R", "S", "T", "U"]
PART = PART_MANUF + PART_SECT                      # partición MECE (33 ramas)

CON = {                                            # contribuciones a Δln(VA_Q/H), p.p.
    "comp_lab":   "LP2ConLC",
    "cap_tic":    "LP2ConTangICT",
    "cap_notic":  "LP2ConTangNICT",
    "cap_intang": "LP2ConIntang",
    "ptf":        "LP2ConTFP",
}
con_ind = {k: load_sheet(GA, v).loc[PART] for k, v in CON.items()}
H_ind = H.loc[PART]

within = {k: [] for k in CON}
for y in DYEARS:
    w0 = H_ind[y - 1] / h_t[y - 1]                # pesos en horas (cobertura 100%)
    w1 = H_ind[y] / h_t[y]
    wbar = (w0 + w1) / 2.0
    for k in CON:
        contr = con_ind[k][y] / 100.0             # p.p. -> fracción
        within[k].append(float((wbar * contr).sum()))
within = pd.DataFrame(within, index=DYEARS)

# between = productividad agregada - suma de los within (reasignación + residuo)
agg = agg.join(within)
agg["between"] = agg["c_prod"] - within.sum(axis=1)

# ---------------------------------------------------------------------------
# 5. Tabla final de componentes (suman exactamente al salario real)
# ---------------------------------------------------------------------------
COMPONENTS = [
    ("c_labshare", "Participación del trabajo"),
    ("comp_lab",   "Composición laboral"),
    ("cap_tic",    "Capital TIC"),
    ("cap_notic",  "Capital no-TIC"),
    ("cap_intang", "Capital intangible"),
    ("ptf",        "PTF (intrasectorial)"),
    ("between",    "Reasignación sectorial"),
    ("c_wedge",    "Cuña de precios"),
]
keys = [k for k, _ in COMPONENTS]
labels = {k: lab for k, lab in COMPONENTS}

annual = agg[keys].copy() * 100.0                  # a puntos porcentuales
annual["Salario real (total)"] = agg["g_real"] * 100.0
annual.index.name = "año"

# control de cuadre
resid = (annual[keys].sum(axis=1) - annual["Salario real (total)"]).abs().max()
print(f"[check] residuo máximo identidad anual: {resid:.2e} p.p.")

# ---------------------------------------------------------------------------
# 6. Etapas
# ---------------------------------------------------------------------------
STAGES = [
    ("1996-2007", "Expansión (ladrillo)", range(1996, 2008)),
    ("2008-2013", "Crisis y devaluación interna", range(2008, 2014)),
    ("2014-2019", "Recuperación", range(2014, 2020)),
    ("2020-2021", "COVID", range(2020, 2022)),
]
stage_rows = []
for code, name, yr in STAGES:
    yrs = [y for y in yr]
    n = len(yrs)
    block = agg.loc[yrs]
    rec = {"etapa": code, "nombre": name, "años": n}
    for k in keys:                                  # media anualizada (p.p./año)
        rec[k] = block[k].mean() * 100.0
    rec["Salario real (total)"] = block["g_real"].mean() * 100.0
    rec["acum_salario_real"] = block["g_real"].sum() * 100.0   # variación acumulada
    stage_rows.append(rec)
stages = pd.DataFrame(stage_rows).set_index("etapa")

# ---------------------------------------------------------------------------
# 7. Estilo y paleta
# ---------------------------------------------------------------------------
plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 11,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.edgecolor": "#555555",
    "axes.titlesize": 14,
    "axes.titleweight": "bold",
    "figure.dpi": 130,
})
COLORS = {
    "c_labshare": "#C0392B",   # rojo terroso
    "comp_lab":   "#27AE60",   # verde
    "cap_tic":    "#85C1E9",   # azul claro
    "cap_notic":  "#3498DB",   # azul medio
    "cap_intang": "#1A5276",   # azul oscuro
    "ptf":        "#8E44AD",   # morado
    "between":    "#7F8C8D",   # gris
    "c_wedge":    "#E67E22",   # ámbar
}

def stacked(ax, df, xlabels, total, title, ylab, xrot=0, bar_w=0.8):
    x = np.arange(len(df))
    pos = np.zeros(len(df)); neg = np.zeros(len(df))
    for k in keys:
        v = df[k].values
        base = np.where(v >= 0, pos, neg)
        ax.bar(x, v, bottom=base, width=bar_w, color=COLORS[k],
               edgecolor="white", linewidth=0.3, label=labels[k], zorder=2)
        pos = pos + np.where(v >= 0, v, 0)
        neg = neg + np.where(v < 0, v, 0)
    ax.plot(x, total, "o-", color="black", lw=1.8, ms=4,
            label="Salario real (total)", zorder=4)
    ax.axhline(0, color="#333333", lw=0.9, zorder=3)
    ax.set_xticks(x); ax.set_xticklabels(xlabels, rotation=xrot,
                                         ha="center" if xrot == 0 else "right")
    ax.set_title(title, loc="left", pad=12)
    ax.set_ylabel(ylab)
    ax.grid(axis="y", color="#E5E5E5", lw=0.8, zorder=0)
    ax.set_axisbelow(True)

# ---------------------------------------------------------------------------
# 8. Gráfico 1: contribuciones anuales
# ---------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(13, 6.6))
stacked(ax, annual, [str(y) for y in annual.index],
        annual["Salario real (total)"].values,
        "Descomposición del crecimiento anual del salario real por hora. España, 1996-2021",
        "Contribución (puntos porcentuales)", xrot=90, bar_w=0.78)
handles, lab = ax.get_legend_handles_labels()
ax.legend(handles, lab, ncol=3, fontsize=9.5, loc="upper center",
          bbox_to_anchor=(0.5, -0.16), frameon=False)
fig.text(0.125, -0.005,
         "Fuente: EUKLEMS & INTANProd 2024 (LLEE) e IPC (INE). "
         "Salario = compensación laboral por hora deflactada por IPC. "
         "Elaboración propia.",
         fontsize=8.5, color="#666666")
fig.tight_layout()
fig.savefig(os.path.join(OUT_IMG_DIR, "g1_descomposicion_anual.png"), bbox_inches="tight", dpi=150)
plt.close(fig)

# ---------------------------------------------------------------------------
# 9. Gráfico 2: por grandes etapas (media anualizada)
# ---------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10.5, 6.6))
xlabels = [f"{code}\n{stages.loc[code,'nombre']}" for code in stages.index]
stacked(ax, stages, xlabels, stages["Salario real (total)"].values,
        "Contribuciones medias anuales por grandes etapas. España",
        "Contribución media (puntos porcentuales por año)", xrot=0, bar_w=0.62)
handles, lab = ax.get_legend_handles_labels()
ax.legend(handles, lab, ncol=3, fontsize=9.5, loc="upper center",
          bbox_to_anchor=(0.5, -0.13), frameon=False)
fig.text(0.125, -0.005,
         "Fuente: EUKLEMS & INTANProd 2024 (LLEE) e IPC (INE). "
         "Media anualizada de las contribuciones; el punto negro es el "
         "crecimiento medio anual del salario real. Elaboración propia.",
         fontsize=8.5, color="#666666")
fig.tight_layout()
fig.savefig(os.path.join(OUT_IMG_DIR, "g2_descomposicion_etapas.png"), bbox_inches="tight", dpi=150)
plt.close(fig)

# ---------------------------------------------------------------------------
# 10. CSVs reproducibles
# ---------------------------------------------------------------------------
csv1 = annual.copy()
csv1.columns = [labels.get(c, c) for c in csv1.columns]
csv1.round(4).to_csv(os.path.join(OUT_DATA_DIR, "datos_descomposicion_anual.csv"),
                     encoding="utf-8-sig")

csv2 = stages.copy()
csv2 = csv2.rename(columns={**labels,
                            "Salario real (total)": "Salario real (total)",
                            "acum_salario_real": "Salario real acumulado etapa"})
csv2.round(4).to_csv(os.path.join(OUT_DATA_DIR, "datos_descomposicion_etapas.csv"),
                     encoding="utf-8-sig")

# ---------------------------------------------------------------------------
# 11. Resumen por consola (para redactar la columna)
# ---------------------------------------------------------------------------
print("\n=== Variación ACUMULADA del salario real por etapa (p.p.) ===")
print(stages[["nombre", "años", "acum_salario_real", "Salario real (total)"]]
      .round(2).to_string())
print("\n=== Contribución media anual por etapa (p.p./año) ===")
print(stages[keys].round(3).to_string())
tot_real = annual["Salario real (total)"].sum()
print(f"\nVariación acumulada salario real 1996-2021: {tot_real:.1f} p.p.")
print("\nContribución acumulada total por factor (p.p., 1996-2021):")
print((annual[keys].sum()).round(2).to_string())
print("\nArchivos generados con éxito.")
