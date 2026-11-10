"""Запуск всех модулей"""

from quantum_tunneling.app import QuantumTunnelingApp
from quantum_tunneling.input import ParameterInput


def main():
    """
    Запрашивает параметры и запускает полный цикл моделирования
    последовательно выполняет расчёт, анимацию
    и сохранение результатов
    """
    params = ParameterInput.read()
    app = QuantumTunnelingApp(params)
    app.run()


if __name__ == "__main__":
    main()
