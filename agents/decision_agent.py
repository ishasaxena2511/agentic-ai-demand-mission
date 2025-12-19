import numpy as np

class DecisionAgent:
    """
    Agent responsible for deciding whether to launch a mission
    based on forecasted demand and confidence.
    """

    def __init__(
        self,
        forecast_values,
        confidence: str,
        horizon: int
    ):
        self.forecast_values = np.array(forecast_values)
        self.confidence = confidence
        self.horizon = horizon

    # -----------------------------
    # Main decision function
    # -----------------------------
    def decide(self):
        avg_demand = self.forecast_values.mean()
        max_demand = self.forecast_values.max()

        # Rule-based, explainable logic
        if avg_demand <= 0:
            return self._no_mission(avg_demand)

        if self.confidence == "Low":
            return self._wait_decision(avg_demand)

        if avg_demand < 20:
            return self._limited_mission(avg_demand)

        return self._full_mission(avg_demand, max_demand)

    # -----------------------------
    # Decision types
    # -----------------------------
    def _no_mission(self, avg):
        return {
            "decision": "NO_MISSION",
            "reason": f"Average forecasted demand is {avg:.2f}, indicating no expected demand.",
            "recommended_action": "Do not launch mission. Monitor demand trends."
        }

    def _wait_decision(self, avg):
        return {
            "decision": "WAIT",
            "reason": f"Forecast confidence is low with average demand {avg:.2f}.",
            "recommended_action": "Wait for more data before committing resources."
        }

    def _limited_mission(self, avg):
        return {
            "decision": "LIMITED_MISSION",
            "reason": f"Moderate demand detected (avg {avg:.2f}).",
            "recommended_action": "Launch a limited-scale mission to test demand."
        }

    def _full_mission(self, avg, peak):
        return {
            "decision": "FULL_MISSION",
            "reason": (
                f"Strong demand forecast detected "
                f"(avg {avg:.2f}, peak {peak:.2f})."
            ),
            "recommended_action": "Launch a full-scale mission."
        }
