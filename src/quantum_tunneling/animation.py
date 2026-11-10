"""Визуализация результатов в GIF."""

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import numpy as np

from .simulation import QuantumSimulation

class QuantumAnimator:
    """Отображает вероятность |psi|² и потенциальный барьер, создаёт GIF."""

    def __init__(self, simulation: QuantumSimulation):
        """
        Подготавливает визуализацию моделирования
        """
        if simulation.densities is None:
            raise ValueError("Сначала вызовите simulation.run()")
        self.simulation = simulation
        self.fig = None
        self.animation = None
        self.line_density = None
        self.time_text = None

    def update(self, frame):
        """
        Обновляет плотность вероятности и время
        """
        s = self.simulation
        self.line_density.set_ydata(s.densities[frame])
        self.time_text.set_text(f"t = {s.times[frame]:.2f}")
        return self.line_density, self.time_text

    def create(self):
        """
        Создаёт график плотности, барьера и объект GIF-анимации
        """
        s = self.simulation
        p = s.params
        self.fig, ax = plt.subplots(figsize=(10, 5))
        ax.set_xlim(p.x_min, p.x_max)
        density_max = float(np.max(s.densities))
        ax.set_ylim(0, max(density_max * 1.25, 1e-12))
        ax.set_xlabel("x")
        ax.set_ylabel(r"$|\psi(x,t)|^2$")
        ax.set_title("Квантовое туннелирование")
        ax.grid(alpha=0.2)
        (self.line_density,) = ax.plot(
            s.x, s.densities[0], linewidth=2, label=r"$|\psi|^2$"
        )

        ax_v = ax.twinx()
        ax_v.set_ylim(min(0, p.V0) * 1.25, max(p.V0, 0) * 1.25 or 1.0)
        ax_v.set_ylabel(r"$V(x)$")
        ax_v.fill_between(s.x, 0, s.V, where=(s.V > 0), color="red", alpha=0.25)
        ax_v.plot(s.x, s.V, color="red", linewidth=1.5, alpha=0.7)
        ax_v.axhline(p.V0, linestyle=":", linewidth=1, alpha=0.6)
        ax_v.text(p.barrier_width / 2 + 0.3, p.V0, rf"$V_0={p.V0}$", va="bottom")

        self.time_text = ax.text(
            0.02, 0.95, f"t = {s.times[0]:.2f}",
            transform=ax.transAxes, fontsize=12, va="top"
        )
        self.animation = FuncAnimation(
            self.fig, self.update, frames=len(s.densities),
            interval=40, blit=False, repeat=True
        )
        return self

    def save(self, output_file):
        """
        Сохранение .gif
        """
        if self.animation is None:
            self.create()
        print(f"Сохранение GIF в {output_file}...")
        try:
            self.animation.save(str(output_file), writer=PillowWriter(fps=25), dpi=100)
        finally:
            plt.close(self.fig)
        print(f"GIF успешно создан! Файл: {output_file}")
