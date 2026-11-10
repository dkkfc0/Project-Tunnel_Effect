"""Запуск всех модулей"""

from quantum_tunneling.app import QuantumTunnelingApp
from quantum_tunneling.input import ParameterInput


def main():
    params = ParameterInput.read()
    app = QuantumTunnelingApp(params)
    app.run()


if __name__ == "__main__":
    main()
