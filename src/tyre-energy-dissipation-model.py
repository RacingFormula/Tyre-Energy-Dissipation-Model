import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class TyreEnergyDissipationModel:
    def __init__(self, config):
        self.tyre_compound = config.get("tyre_compound", "soft")
        self.track_temperature = config.get("track_temperature", 25)  # degrees Celsius
        self.initial_tyre_temp = config.get("initial_tyre_temp", 70)  # degrees Celsius
        self.lateral_force = config.get("lateral_force", 4000)  # Newtons
        self.longitudinal_force = config.get("longitudinal_force", 3000)  # Newtons
        self.degradation_rate = config.get("degradation_rate", 0.001)  # percentage per lap
        self.race_distance = config.get("race_distance", 50)  # laps
        self.ambient_temperature = config.get("ambient_temperature", 20)  # degrees Celsius
        self.tyre_heat_capacity = config.get("tyre_heat_capacity", 1.2)  # J/(g*K)

    def calculate_tyre_energy_dissipation(self, lap):
        lateral_energy = 0.5 * self.lateral_force ** 2 / 1000  # simplified energy dissipation formula
        longitudinal_energy = 0.5 * self.longitudinal_force ** 2 / 1000
        total_energy = lateral_energy + longitudinal_energy

        degradation_factor = 1 - (lap * self.degradation_rate)
        total_energy *= degradation_factor

        return total_energy

    def simulate_tyre_temperature(self, energy_dissipation, current_temp):
        heat_transfer = energy_dissipation / self.tyre_heat_capacity
        heat_loss = (current_temp - self.ambient_temperature) * 0.05
        new_temp = current_temp + heat_transfer - heat_loss
        return new_temp

    def run_simulation(self):
        results = []
        current_tyre_temp = self.initial_tyre_temp

        for lap in range(1, self.race_distance + 1):
            energy_dissipation = self.calculate_tyre_energy_dissipation(lap)
            current_tyre_temp = self.simulate_tyre_temperature(energy_dissipation, current_tyre_temp)

            results.append({
                "lap": lap,
                "energy_dissipation": energy_dissipation,
                "tyre_temperature": current_tyre_temp
            })

        return pd.DataFrame(results)

    def plot_results(self, results_df):
        plt.figure(figsize=(12, 6))
        plt.plot(results_df["lap"], results_df["energy_dissipation"], label="Energy Dissipation (kJ)")
        plt.plot(results_df["lap"], results_df["tyre_temperature"], label="Tyre Temperature (°C)")
        plt.xlabel("Lap")
        plt.ylabel("Values")
        plt.title("Tyre Energy Dissipation and Temperature Over Race Distance")
        plt.legend()
        plt.grid(True)
        plt.show()

if __name__ == "__main__":
    config = {
        "tyre_compound": "soft",
        "track_temperature": 30,
        "initial_tyre_temp": 80,
        "lateral_force": 4500,
        "longitudinal_force": 3500,
        "degradation_rate": 0.002,
        "race_distance": 50,
        "ambient_temperature": 25,
        "tyre_heat_capacity": 1.1,
    }

    model = TyreEnergyDissipationModel(config)
    results_df = model.run_simulation()

    print("Simulation Results:")
    print(results_df.head())

    model.plot_results(results_df)