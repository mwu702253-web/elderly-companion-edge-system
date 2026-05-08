import math
import random

class FallDetector:
    def calculate_score(self, keypoints: dict) -> dict:
        shoulder = keypoints["shoulder"]
        hip = keypoints["hip"]

        dx = abs(shoulder[0] - hip[0])
        dy = abs(shoulder[1] - hip[1])
        body_angle = math.degrees(math.atan2(dy, dx + 1e-6))

        score = 0
        reasons = []

        if body_angle < 35:
            score += 45
            reasons.append("Body is close to horizontal posture")

        if hip[1] < shoulder[1]:
            score += 20
            reasons.append("Hip position is abnormal relative to shoulder")

        if random.random() > 0.65:
            score += 25
            reasons.append("Simulated sudden posture change detected")

        if score >= 60:
            risk_level = "High"
        elif score >= 35:
            risk_level = "Medium"
        else:
            risk_level = "Low"

        return {
            "score": score,
            "risk_level": risk_level,
            "reason": "; ".join(reasons) if reasons else "No obvious fall-risk pattern detected",
        }

    def detect_from_simulated_keypoints(self) -> dict:
        scenario = random.choice(["standing", "sitting", "falling"])

        if scenario == "falling":
            keypoints = {"shoulder": (120, 210), "hip": (260, 230)}
        elif scenario == "sitting":
            keypoints = {"shoulder": (180, 160), "hip": (190, 250)}
        else:
            keypoints = {"shoulder": (180, 120), "hip": (185, 260)}

        result = self.calculate_score(keypoints)
        result["scenario"] = scenario
        return result
