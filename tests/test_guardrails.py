import pytest
import sys
import os

# Ensure the src module can be imported
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.guardrails import check_guardrails, detect_pii, is_advisory_query

class TestPIIDetection:
    def test_pan_detected(self):
        assert detect_pii("My PAN is ABCDE1234F") == True

    def test_aadhaar_detected(self):
        assert detect_pii("Aadhaar: 1234 5678 9012") == True

    def test_phone_detected(self):
        assert detect_pii("Call me at 9876543210") == True

    def test_email_detected(self):
        assert detect_pii("Send to user@example.com") == True

    def test_clean_query_passes(self):
        assert detect_pii("What is the expense ratio?") == False


class TestAdvisoryDetection:
    def test_should_i_invest(self):
        assert is_advisory_query("Should I invest in HSBC Midcap?") == True

    def test_which_is_better(self):
        assert is_advisory_query("Which fund is better?") == True

    def test_recommend(self):
        assert is_advisory_query("Can you recommend a fund?") == True

    def test_factual_passes(self):
        assert is_advisory_query("What is the exit load?") == False


class TestGuardrailsIntegration:
    def test_factual_allowed(self):
        result = check_guardrails("What is the expense ratio of HSBC Midcap Fund?")
        assert result["allowed"] == True

    def test_advisory_blocked(self):
        result = check_guardrails("Should I invest in HSBC Midcap?")
        assert result["allowed"] == False
        assert result["reason"] == "advisory"

    def test_pii_blocked(self):
        result = check_guardrails("My PAN is ABCDE1234F, what about my fund?")
        assert result["allowed"] == False
        assert result["reason"] == "pii"

    def test_off_topic_blocked(self):
        result = check_guardrails("What is the weather today?")
        assert result["allowed"] == False
        assert result["reason"] == "off_topic"
