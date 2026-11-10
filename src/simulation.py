"""Численный расчёт волнового пакета."""

import numpy as np
import wavepacket as wp

from .parameters import SimulationParams

class QuantumSimulation:
    """Строит гамильтониан и рассчитывает эволюцию волнового пакета."""

    def __init__(self, params: SimulationParams):
        self.params = params
        self.grid = None
        self.x = None
        self.V = None
        self.times = None
        self.densities = None

    def potential(self, x):
        """Прямоугольный барьер, расположенный симметрично относительно x=0."""
        p = self.params
        return np.where(np.abs(x) <= p.barrier_width / 2, p.V0, 0.0)

    def run(self):
        p = self.params
        dof = wp.grid.PlaneWaveDof(p.x_min, p.x_max, p.N)
        self.grid = wp.grid.Grid(dof)
        dx = (p.x_max - p.x_min) / p.N
        self.x = p.x_min + dx * np.arange(p.N)
        self.V = self.potential(self.x)

        kinetic = wp.operator.CartesianKineticEnergy(self.grid, 0, mass=p.mass)
        potential_op = wp.operator.Potential1D(self.grid, 0, self.potential)
        hamiltonian = kinetic + potential_op

        gaussian = wp.special.Gaussian(
            p.x0, rms=p.sigma / np.sqrt(2.0), p=p.k0
        )
        psi0 = wp.normalize(wp.builder.product_wave_function(self.grid, gaussian))

        equation = wp.expression.SchroedingerEquation(hamiltonian)
        solver = wp.solver.OdeSolver(equation, dt=p.dt, rtol=1e-7, atol=1e-9)

        print("Расчёт эволюции...")
        propagation = list(solver.propagate(psi0, t0=0.0, num_steps=p.num_steps))
        if not propagation:
            raise RuntimeError("Решатель не вернул ни одного состояния")

        frame_indices = np.arange(0, len(propagation), p.frame_step)
        self.times = np.array([propagation[i][0] for i in frame_indices])
        self.densities = np.array([
            wp.dvr_density(propagation[i][1]) for i in frame_indices
        ])
        print(f"Расчёт завершён. Получено состояний: {len(propagation)}")
        print(f"Кадров GIF: {len(self.times)}")
        print("|psi|² рассчитано.")
        return self
