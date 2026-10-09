import unittest

from main import explain_risk


class ExplainRiskTests(unittest.TestCase):
    def test_link_is_flagged(self):
        results = explain_risk("Please review https://example.com")
        self.assertTrue(any(item["title"] == "Contains a link" for item in results))

    def test_credential_request_is_flagged(self):
        results = explain_risk("Urgent, send your OTP immediately")
        titles = {item["title"] for item in results}
        self.assertIn("Credential or secret request", titles)
        self.assertIn("Urgency or account threat", titles)

    def test_plain_message_does_not_get_high_severity(self):
        results = explain_risk("The meeting starts at 10 tomorrow.")
        self.assertFalse(any(item["severity"] == "high" for item in results))


if __name__ == "__main__":
    unittest.main()
