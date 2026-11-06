"""
Unit tests for NaturalTest framework.
Verifies configuration, heuristic planner, assertion evaluation, and DOM extraction logic.
"""

import unittest
from natural_test.config import TestConfig
from natural_test.models.heuristic import HeuristicProvider
from natural_test.models.base import ActionDecision, AssertionResult
from natural_test.reporter.html_reporter import generate_html_report
from natural_test.agent.executor import TestResult, StepResult


class TestNaturalTest(unittest.TestCase):

    def setUp(self):
        self.provider = HeuristicProvider()

    def test_config_defaults(self):
        config = TestConfig()
        self.assertTrue(config.headless)
        self.assertEqual(config.browser_type, "chromium")
        self.assertEqual(config.resolve_provider(), "heuristic")

    def test_heuristic_login_planning(self):
        goal = "Log in as a customer and verify the dashboard is shown"
        page_state = {
            "url": "https://example.com/login",
            "title": "Login Page",
            "headings": ["Please sign in"],
            "interactive_elements": [
                {"tag": "input", "type": "email", "id": "email", "name": "email", "selector": "#email"},
                {"tag": "input", "type": "password", "id": "password", "name": "password", "selector": "#password"},
                {"tag": "button", "type": "submit", "selector": "button[type='submit']", "text": "Sign In"}
            ]
        }

        # Step 1: Should fill email
        history = []
        decision = self.provider.decide_next_step(goal, history, page_state)
        self.assertEqual(decision.action, "fill")
        self.assertIn("user@phptravels.com", decision.value)

        # Step 2: After email filled, should fill password
        history.append({"action": "fill", "selector": "#email", "value": decision.value, "result": "SUCCESS"})
        decision2 = self.provider.decide_next_step(goal, history, page_state)
        self.assertEqual(decision2.action, "fill")
        self.assertIn("demouser", decision2.value)

        # Step 3: After password filled, should submit credentials
        history.append({"action": "fill", "selector": "#password", "value": decision2.value, "result": "SUCCESS"})
        decision3 = self.provider.decide_next_step(goal, history, page_state)
        self.assertEqual(decision3.action, "click")
        self.assertIn("submit", decision3.selector)

    def test_assertion_verification(self):
        page_state = {
            "url": "https://phptravels.net/dashboard",
            "title": "Customer Dashboard",
            "headings": ["Welcome, Customer", "Recent Bookings"],
            "interactive_elements": [],
            "body_snippet": "Dashboard account overview"
        }

        res = self.provider.verify_assertion("verify the dashboard is shown", page_state)
        self.assertTrue(res.passed)
        self.assertIn("Dashboard", res.reason)

    def test_checkbox_assertion(self):
        page_state = {
            "url": "https://example.com/checkboxes",
            "title": "Checkboxes",
            "headings": [],
            "interactive_elements": [
                {"tag": "input", "type": "checkbox", "checked": True, "selector": "input:nth-child(1)"}
            ],
            "body_snippet": ""
        }

        res = self.provider.verify_assertion("verify it is checked", page_state)
        self.assertTrue(res.passed)

    def test_html_report_generation(self):
        result = TestResult(
            test_case="Log in as customer",
            url="https://phptravels.net",
            status="PASSED",
            duration_seconds=5.2,
            steps=[
                StepResult(step_number=1, action="navigate", selector=None, value="https://phptravels.net", reason="Navigated", status="SUCCESS", duration_ms=1200)
            ],
            assertions=[
                AssertionResult(passed=True, assertion_text="dashboard is shown", expected="dashboard", actual="dashboard", reason="matches")
            ]
        )
        report_path = generate_html_report(result)
        self.assertTrue(report_path.endswith(".html"))


if __name__ == "__main__":
    unittest.main()

