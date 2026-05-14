"""
================================================================
plot_contour.py  (CORRIGIDO)
Gera o Contour Plot da função de Rastrigin (n=2) com as
posições das partículas sobrepostas em cada iteração.

Dependências:
    pip install matplotlib numpy pandas
================================================================
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import pandas as pd
import os

# ─────────────────────────────────────────
# CONFIGURAÇÃO — altere aqui o cenário desejado
# Opções: c1_0_c2_1 | c1_1_c2_0 | c1_1_c2_1
#         c1_1_c2_01 | c1_2_c2_2 | c1_4_c2_4
# ─────────────────────────────────────────
SCENARIO   = "c1_2_c2_2"
CSV_FILE   = f"positions_{SCENARIO}.csv"
OUTPUT_PNG = f"contour_{SCENARIO}.png"

# ─────────────────────────────────────────
# 1. Função de Rastrigin
# ─────────────────────────────────────────
def rastrigin(x, y, A=10):
    return (A * 2
            + x**2 - A * np.cos(2 * np.pi * x)
            + y**2 - A * np.cos(2 * np.pi * y))

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

df = pd.read_csv(CSV_FILE)
for iter_num, group in df.groupby("Iteracao"):
    particles_iter[iter_num] = (group["X0"].values, group["X1"].values)
print(f"[INFO] '{CSV_FILE}' carregado — {len(particles_iter)} iterações.")

# ─────────────────────────────────────────
# 4. Figura com 4 snapshots: iter 1, 25, 50, 100
# ─────────────────────────────────────────
snapshots  = [1, 25, 50, 100]
fig, axes  = plt.subplots(2, 2, figsize=(13, 11))
fig.suptitle(f"PSO — Rastrigin (n=2) | Cenário: {SCENARIO.replace('_',' ')}",
             fontsize=15, fontweight="bold")
fig.patch.set_facecolor("#0d0d1a")

for ax, it in zip(axes.flat, snapshots):
    ax.set_facecolor("#0d0d1a")
    cp = ax.contourf(X, Y, Z, levels=60, cmap="plasma", alpha=0.9)
    ax.contour(X, Y, Z, levels=25, colors="white", linewidths=0.3, alpha=0.25)

    # Mínimo global
    ax.plot(0, 0, "r*", markersize=14, zorder=6, label="Ótimo (0,0)")

    # Partículas
    real_it = min(it, max(particles_iter.keys()))
    if real_it in particles_iter:
        px, py = particles_iter[real_it]
        ax.scatter(px, py, c="cyan", edgecolors="white",
                   s=55, zorder=7, label="Partículas")

    ax.set_xlim(-5.12, 5.12)
    ax.set_ylim(-5.12, 5.12)
    ax.set_xlabel("x₀", color="white", fontsize=10)
    ax.set_ylabel("x₁", color="white", fontsize=10)
    ax.set_title(f"Iteração {real_it}", color="white", fontsize=12)
    ax.tick_params(colors="white")
    for spine in ax.spines.values():
        spine.set_edgecolor("#444")
    ax.legend(loc="upper right", fontsize=7,
              facecolor="#1a1a2e", labelcolor="white")

plt.colorbar(cp, ax=axes, label="f(x₀, x₁)", shrink=0.6, pad=0.02)
plt.tight_layout()
plt.savefig(OUTPUT_PNG, dpi=150, facecolor=fig.get_facecolor())
print(f"[OK] Contour plot salvo: {OUTPUT_PNG}")
plt.show()
