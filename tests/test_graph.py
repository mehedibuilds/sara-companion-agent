from sara.graph import classify
from sara.models import Intent

def test_routes_coding_request() -> None:
    assert classify("Can you debug this Python API?") is Intent.CODE

def test_defaults_to_chat() -> None:
    assert classify("How are you today?") is Intent.CHAT