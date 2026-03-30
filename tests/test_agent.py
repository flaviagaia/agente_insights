from __future__ import annotations

import unittest

from src.agent import ask_business_insights_agent
from src.sample_data import ensure_sample_data
from src.tools import compute_growth_diagnostics, suggest_business_actions


class BusinessInsightsAgentTests(unittest.TestCase):
    def setUp(self) -> None:
        ensure_sample_data()

    def test_growth_diagnostics_exposes_flags(self) -> None:
        diagnostics = compute_growth_diagnostics("BIZ-1002")
        self.assertIn("growth_pct", diagnostics)
        self.assertIn("risk_flags", diagnostics)
        self.assertGreaterEqual(len(diagnostics["risk_flags"]), 1)

    def test_suggest_business_actions_returns_priorities(self) -> None:
        actions = suggest_business_actions("BIZ-1001")
        self.assertIn("priority_actions", actions)
        self.assertGreaterEqual(len(actions["priority_actions"]), 1)

    def test_agent_returns_final_message(self) -> None:
        result = ask_business_insights_agent(
            company_id="BIZ-1003",
            user_question="Quais sinais executivos mais importantes aparecem neste trimestre?",
        )
        self.assertIn("runtime_mode", result)
        self.assertIn("final_message", result)
        self.assertIn("Insight executivo", result["final_message"])


if __name__ == "__main__":
    unittest.main()
