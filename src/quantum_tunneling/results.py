"""Сохранение параметров и массивов."""

from dataclasses import asdict
import json
from pathlib import Path

import numpy as np

from .simulation import QuantumSimulation

class ResultsSaver:
    """Выбирает уникальное имя и сохраняет параметры и численные данные."""

    def __init__(self, results_dir="results", data_dir="data"):
        self.results_dir = Path(results_dir)
        self.data_dir = Path(data_dir)
        self.results_dir.mkdir(parents=True, exist_ok=True)
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def next_gif_path(self, base_name="quantum_tunneling"):
        path = self.results_dir / f"{base_name}.gif"
        counter = 1
        while path.exists():
            path = self.results_dir / f"{base_name} ({counter}).gif"
            counter += 1
        return path

    def save_data(self, simulation: QuantumSimulation, output_file):
        stem = Path(output_file).stem
        params = asdict(simulation.params)
        params["output_file"] = str(output_file)
        json_path = self.data_dir / f"{stem}.json"
        with json_path.open("w", encoding="utf-8") as file:
            json.dump(params, file, indent=4, ensure_ascii=False)
        print(f"Параметры сохранены в {json_path}")

        for name in ("x", "V", "times", "densities"):
            path = self.data_dir / f"{stem}_{name}.npy"
            np.save(path, getattr(simulation, name))
            print(f"  сохранено: {path}")
