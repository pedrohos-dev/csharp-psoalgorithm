"""
================================================================
plot_contour.py  
Gera o Contour Plot da função de Rastrigin (n=2) com as
posições das partículas sobrepostas em cada iteração.

Dependências:
    pip install matplotlib numpy pandas
================================================================
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os

plt.style.use('dark_background')

# ─────────────────────────────────────────
# CONFIGURAÇÃO — altere aqui o cenário desejado
# Opções: c1_0_c2_1 | c1_1_c2_0 | c1_1_c2_1
#         c1_1_c2_01 | c1_2_c2_2 | c1_4_c2_4
# ─────────────────────────────────────────
SCENARIO   = "c1_4_c2_4"
CSV_FILE   = f"particle-positions-csv/positions_{SCENARIO}.csv"
OUTPUT_PNG = f"particle-plots-png/contour_{SCENARIO}.png"

# ─────────────────────────────────────────
# 1. Função de Rastrigin
# ─────────────────────────────────────────
def rastrigin(x, y, A=10):
    return (A * 2
            + x**2 - A * np.cos(2 * np.pi * x)
            + y**2 - A * np.cos(2 * np.pi * y))


def load_positions(file_path):
    return pd.read_csv(file_path, dtype={"Iteracao": int, "Particula": int})

# ─────────────────────────────────────────
# 2. Grade para o contour plot
# ─────────────────────────────────────────
resolution = 500
x_vals = np.linspace(-5.12, 5.12, resolution)
y_vals = np.linspace(-5.12, 5.12, resolution)
X, Y   = np.meshgrid(x_vals, y_vals)
Z      = rastrigin(X, Y)

# ─────────────────────────────────────────
# 3. Lê posições das partículas
# ─────────────────────────────────────────
particles_iter = {}

if not os.path.exists(CSV_FILE):
    print(f"[ERRO] Arquivo '{CSV_FILE}' não encontrado.")
    print("Execute 'dotnet run' no projeto C# primeiro para gerar os CSVs.")
    exit(1)

try:
    df = load_positions(CSV_FILE)
except ValueError as exc:
    print(f"[ERRO] {exc}")
    exit(1)

for iter_num, group in df.groupby("Iteracao"):
    particles_iter[iter_num] = (group["X0"].values, group["X1"].values)
print(f"[INFO] '{CSV_FILE}' carregado — {len(particles_iter)} iterações.")

# ─────────────────────────────────────────
# 4. Figura com 4 snapshots ao longo do histórico disponível
# ─────────────────────────────────────────
max_iter = max(particles_iter.keys())
snapshots = [1,
             max(1, max_iter // 3),
             max(1, (2 * max_iter) // 3),
             max_iter]
fig, axes = plt.subplots(2, 2, figsize=(13, 11), constrained_layout=True)
fig.suptitle(
    f"PSO — Rastrigin (n=2) | Cenário: {SCENARIO.replace('_',' ')} "
    f"| Iterações: {max_iter} | Partículas: {len(df['Particula'].unique())}",
    fontsize=16,
    fontweight="bold",
    color="white"
)
fig.patch.set_facecolor("#0d0d1a")

for ax, it in zip(axes.flat, snapshots):
    ax.set_facecolor("#0d0d1a")
    cp = ax.contourf(
        X,
        Y,
        Z,
        levels=45,
        cmap="magma",
        alpha=0.92,
        antialiased=True,
    )
    ax.contour(
        X,
        Y,
        Z,
        levels=20,
        colors="white",
        linewidths=0.25,
        alpha=0.35,
    )

    # Mínimo global
    ax.plot(0, 0, "*", markersize=16, color="#ff5555", zorder=8, label="Ótimo (0,0)")

    # Partículas
    real_it = min(it, max(particles_iter.keys()))
    if real_it in particles_iter:
        px, py = particles_iter[real_it]
        ax.scatter(
            px,
            py,
            c="#4dd2ff",
            edgecolors="white",
            linewidths=0.9,
            s=90,
            alpha=0.92,
            zorder=7,
            label="Partículas",
        )

    ax.set_xlim(-5.12, 5.12)
    ax.set_ylim(-5.12, 5.12)
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlabel("x₀", color="white", fontsize=11)
    ax.set_ylabel("x₁", color="white", fontsize=11)
    ax.set_title(f"Iteração {real_it}", color="#ffffff", fontsize=13, pad=9)
    ax.tick_params(colors="white", labelsize=9)
    ax.grid(color="#333333", linestyle="--", linewidth=0.4, alpha=0.35)
    for spine in ax.spines.values():
        spine.set_edgecolor("#666666")
    ax.legend(
        loc="upper right",
        fontsize=8,
        facecolor="#1a1a2e",
        edgecolor="#444444",
        labelcolor="white",
    )

cbar = fig.colorbar(cp, ax=axes, label="f(x₀, x₁)", shrink=0.66, pad=0.02)
cbar.outline.set_color("white")
cbar.ax.yaxis.set_tick_params(color="white")
plt.setp(plt.getp(cbar.ax.axes, "yticklabels"), color="white")

plt.savefig(OUTPUT_PNG, dpi=180, facecolor=fig.get_facecolor())
print(f"[OK] Contour plot salvo: {OUTPUT_PNG}")
plt.show()
