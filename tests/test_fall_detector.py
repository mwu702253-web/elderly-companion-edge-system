from app.vision.fall_detector import FallDetector

def test_fall_detector_returns_valid_result():
    detector = FallDetector()
    result = detector.detect_from_simulated_keypoints()
    assert result["risk_level"] in ["Low", "Medium", "High"]
    assert isinstance(result["score"], int)
    assert isinstance(result["reason"], str)
