"""Оркестрация этапов моделирования."""

from .parameters import SimulationParams
from .simulation import QuantumSimulation
from .animation import QuantumAnimator
from .results import ResultsSaver

class QuantumTunnelingApp:
    """Координирует запуск моделирования, анимацию и экспорт."""

    def __init__(self, params: SimulationParams):
        """
        Создаёт компоненты расчёта и сохранения результатов
        """
        self.simulation = QuantumSimulation(params)
        self.saver = ResultsSaver()

    def run(self):
        """
        Запускает расчёт, создание GIF и экспорт численных данных
        """
        self.simulation.run()
        output_file = self.saver.next_gif_path()
        QuantumAnimator(self.simulation).create().save(output_file)
        self.saver.save_data(self.simulation, output_file)
        return output_file
