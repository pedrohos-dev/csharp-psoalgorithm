"""
================================================================
generate_video.py  (CORRIGIDO)
Gera um vídeo .mp4 (ou GIF) mostrando a evolução do enxame
sobre o contour plot da Rastrigin nas 100 iterações.

Dependências:
    pip install matplotlib numpy pandas
    ffmpeg no PATH  → gera MP4
    pip install pillow → gera GIF (fallback automático)
================================================================
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd
import os
import sys

# ─────────────────────────────────────────
# CONFIGURAÇÃO — altere aqui o cenário desejado
# Opções: c1_0_c2_1 | c1_1_c2_0 | c1_1_c2_1
#         c1_1_c2_01 | c1_2_c2_2 | c1_4_c2_4
# ─────────────────────────────────────────
SCENARIO        = "c1_2_c2_2"
CSV_POSITIONS   = f"positions_{SCENARIO}.csv"
CSV_CONVERGENCE = "convergence_all.csv"
OUTPUT_MP4      = f"pso_{SCENARIO}.mp4"
OUTPUT_GIF      = f"pso_{SCENARIO}.gif"
FPS             = 10
INTERVAL_MS     = 100

# ─────────────────────────────────────────
# 1. Carrega posições
# ─────────────────────────────────────────
if not os.path.exists(CSV_POSITIONS):
    print(f"[ERRO] Arquivo '{CSV_POSITIONS}' não encontrado.")
    print("Execute 'dotnet run' no projeto C# primeiro.")
    sys.exit(1)

df = pd.read_csv(CSV_POSITIONS)
iterations = sorted(df["Iteracao"].unique())
particles_by_iter = {
    it: (df[df["Iteracao"] == it]["X0"].values,
         df[df["Iteracao"] == it]["X1"].values)
    for it in iterations
}
print(f"[INFO] '{CSV_POSITIONS}' carregado — {len(iterations)} iterações, "
      f"{len(df[df['Iteracao']==iterations[0]])} partículas.")

# ─────────────────────────────────────────
# 2. Carrega curva de fitness
# ─────────────────────────────────────────
fitness_curve = None
if os.path.exists(CSV_CONVERGENCE):
    cdf = pd.read_csv(CSV_CONVERGENCE)
    # A coluna tem o mesmo nome da key usada no C#
    if SCENARIO in cdf.columns:
        fitness_curve = cdf[SCENARIO].values
        print(f"[INFO] Curva de fitness carregada — coluna '{SCENARIO}'.")
    else:
        print(f"[AVISO] Coluna '{SCENARIO}' não encontrada em {CSV_CONVERGENCE}.")
        print(f"        Colunas disponíveis: {list(cdf.columns)}")

# ─────────────────────────────────────────
# 3. Grid da Rastrigin
# ─────────────────────────────────────────
def rastrigin(x, y, A=10):
    return (A * 2
            + x**2 - A * np.cos(2 * np.pi * x)
            + y**2 - A * np.cos(2 * np.pi * y))

res = 300
xv  = np.linspace(-5.12, 5.12, res)
yv  = np.linspace(-5.12, 5.12, res)
X, Y = np.meshgrid(xv, yv)
Z    = rastrigin(X, Y)

# ─────────────────────────────────────────
# 4. Monta a figura
# ─────────────────────────────────────────
has_fitness = fitness_curve is not None
if has_fitness:
    fig, (ax_main, ax_fit) = plt.subplots(
        1, 2, figsize=(13, 5.5),
        gridspec_kw={"width_ratios": [1.1, 0.9]}
    )
else:
    fig, ax_main = plt.subplots(figsize=(7, 6))
    ax_fit = None

fig.patch.set_facecolor("#1a1a2e")

# ── Contour ───────────────────────────────
ax_main.set_facecolor("#1a1a2e")
cp = ax_main.contourf(X, Y, Z, levels=60, cmap="plasma", alpha=0.9)
ax_main.contour(X, Y, Z, levels=25, colors="white", linewidths=0.3, alpha=0.3)
plt.colorbar(cp, ax=ax_main, label="f(x₀, x₁)", pad=0.02)
ax_main.plot(0, 0, "r*", markersize=16, label="Ótimo global (0,0)", zorder=6)
ax_main.set_xlim(-5.12, 5.12)
ax_main.set_ylim(-5.12, 5.12)
ax_main.set_xlabel("x₀", color="white", fontsize=11)
ax_main.set_ylabel("x₁", color="white", fontsize=11)
ax_main.tick_params(colors="white")
for spine in ax_main.spines.values():
    spine.set_edgecolor("white")

scat = ax_main.scatter([], [], c="cyan", edgecolors="white",
                       s=55, zorder=7, label="Partículas")
ax_main.legend(loc="upper right", fontsize=8,
               facecolor="#1a1a2e", labelcolor="white")
title_txt = ax_main.set_title("", color="white", fontsize=13)

# ── Fitness ───────────────────────────────
fit_line = None
if ax_fit is not None:
    ax_fit.set_facecolor("#1a1a2e")
    ax_fit.set_xlim(0, len(iterations) + 1)
    ymax = float(fitness_curve[0]) * 1.1 if fitness_curve is not None else 100
    ax_fit.set_ylim(-1, ymax)
    ax_fit.set_xlabel("Iteração", color="white", fontsize=10)
    ax_fit.set_ylabel("Melhor Fitness", color="white", fontsize=10)
    ax_fit.set_title(f"Convergência — {SCENARIO.replace('_',' ')}",
                     color="white", fontsize=11)
    ax_fit.tick_params(colors="white")
    for spine in ax_fit.spines.values():
        spine.set_edgecolor("white")
    fit_line, = ax_fit.plot([], [], color="lime", lw=2, label="gbest fitness")
    ax_fit.axhline(0, color="red", lw=1.5, linestyle="--",
                   alpha=0.7, label="f=0 (ótimo global)")
    ax_fit.legend(fontsize=8, facecolor="#1a1a2e", labelcolor="white")

plt.tight_layout()

# ─────────────────────────────────────────
# 5. Função de animação
# ─────────────────────────────────────────
def animate(frame):
    it = iterations[frame]
    px, py = particles_by_iter[it]
    scat.set_offsets(np.c_[px, py])
    title_txt.set_text(
        f"PSO — Rastrigin  |  Iteração {it:>3d} / {len(iterations)}"
    )
    if fit_line is not None and fitness_curve is not None:
        fit_line.set_data(range(1, frame + 2), fitness_curve[:frame + 1])
        return scat, title_txt, fit_line
    return scat, title_txt

# ─────────────────────────────────────────
# 6. Renderiza
# ─────────────────────────────────────────
ani = animation.FuncAnimation(
    fig,
    animate,
    frames=len(iterations),
    interval=INTERVAL_MS,
    blit=True
)

saved = False

# Tenta MP4 (ffmpeg)
try:
    writer = animation.FFMpegWriter(fps=FPS, bitrate=1800)
    ani.save(OUTPUT_MP4, writer=writer, dpi=120)
    print(f"[OK] Vídeo MP4 salvo: {OUTPUT_MP4}")
    saved = True
except Exception as e:
    print(f"[AVISO] ffmpeg não disponível: {e}")

# Fallback: GIF via pillow
if not saved:
    try:
        ani.save(OUTPUT_GIF, writer="pillow", fps=FPS, dpi=100)
        print(f"[OK] GIF salvo: {OUTPUT_GIF}")
        saved = True
    except Exception as e:
        print(f"[ERRO] Não foi possível salvar nem MP4 nem GIF: {e}")
        print("Instale ffmpeg (https://ffmpeg.org/download.html) ou: pip install pillow")

plt.close()
