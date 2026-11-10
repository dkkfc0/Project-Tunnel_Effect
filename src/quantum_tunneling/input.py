"""Ввод физических параметров."""

from .parameters import SimulationParams

class ParameterInput:
    """Интерактивный ввод параметров с проверкой."""

    @staticmethod
    def get_number(prompt):
        while True:
            try:
                return float(input(prompt + " ").replace(",", "."))
            except ValueError:
                print("Ошибка. Введите число.")

    @classmethod
    def read(cls):
        print("Задайте начальные условия системы")
        while True:
            x_min = cls.get_number("Координата минимума оси X:")
            x_max = cls.get_number("Координата максимума оси X:")
            if x_min < x_max:
                break
            print("Ошибка: максимум оси X должен быть больше минимума.")

        while True:
            mass = cls.get_number("Масса частицы:")
            if mass > 0:
                break
            print("Ошибка: масса должна быть положительной.")

        while True:
            x0 = cls.get_number("Координата точки начала движения волны:")
            if x_min <= x0 <= x_max:
                break
            print(f"Ошибка: x0 = {x0} вне диапазона [{x_min}, {x_max}].")

        k0 = cls.get_number("Кинетическая энергия волны (параметр p):")
        V0 = cls.get_number("Потенциальная энергия барьера:")
        while True:
            barrier_width = cls.get_number("Ширина барьера по оси X:")
            if barrier_width > 0:
                break
            print("Ошибка: ширина барьера должна быть положительной.")

        return SimulationParams(
            x_min=x_min, x_max=x_max, mass=mass, x0=x0,
            k0=k0, V0=V0, barrier_width=barrier_width,
        )
