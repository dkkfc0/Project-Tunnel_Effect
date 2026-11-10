"""Параметры расчёта"""

from dataclasses import dataclass

@dataclass
class SimulationParams:
    """Настройки физической модели и численного расчёта."""

    x_min: float
    x_max: float
    mass: float
    x0: float
    k0: float
    V0: float
    barrier_width: float
    N: int = 256
    sigma: float = 0.8
    dt: float = 0.01
    num_steps: int = 1200
    frame_step: int = 10

    def __post_init__(self):
        """
        Проверяет значения параметров после создания объекта.
        
        Исключения: ValueError: если введённые численные настройки недопустимы.
        """
        if self.x_min >= self.x_max:
            raise ValueError("x_min должен быть меньше x_max")
        if self.mass <= 0:
            raise ValueError("Масса должна быть положительной")
        if not self.x_min <= self.x0 <= self.x_max:
            raise ValueError("Начальная координата x0 должна принадлежать диапазону X")
        if self.barrier_width <= 0:
            raise ValueError("Ширина барьера должна быть положительной")
        if self.sigma <= 0 or self.dt <= 0:
            raise ValueError("sigma и dt должны быть положительными")
        if self.N < 2 or self.num_steps < 1 or self.frame_step < 1:
            raise ValueError("N >= 2, num_steps >= 1 и frame_step >= 1 обязательны")

