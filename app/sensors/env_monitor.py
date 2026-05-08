import random
from datetime import datetime

class EnvironmentMonitor:
    def __init__(self, simulation: bool = True):
        self.simulation = simulation

    def read(self) -> dict:
        if self.simulation:
            return {
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "temperature": round(random.uniform(20, 33), 1),
                "humidity": round(random.uniform(35, 85), 1),
                "smoke": round(random.uniform(0, 1), 2),
                "gas": round(random.uniform(0, 1), 2),
            }

        raise NotImplementedError("Real sensor adapter is not implemented in this public demo.")

    def analyze(self, record: dict) -> str:
        alerts = []

        if record["temperature"] >= 30:
            alerts.append("High temperature")
        if record["humidity"] >= 75:
            alerts.append("High humidity")
        if record["smoke"] >= 0.75:
            alerts.append("Smoke risk")
        if record["gas"] >= 0.75:
            alerts.append("Gas risk")

        return "Normal" if not alerts else ", ".join(alerts)
