def evaluate_status(violations: list) -> str:
    HIGH_COUNT_THRESHOLD = 3
    critical_count = sum(1 for v in violations if v.get("severity", "").lower() == "critical")
    high_count = sum(1 for v in violations if v.get("severity", "").lower() == "high")
    if critical_count > 0 or high_count >= HIGH_COUNT_THRESHOLD:
        return "above_threshold:critical"
    return "within_threshold:good"
