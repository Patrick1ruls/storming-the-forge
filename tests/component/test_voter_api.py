import pytest
import requests

VOTER_URL = "http://localhost:5555/"

@pytest.mark.parametrize("vote", [
    "a", 
    "b",
    "vote=-1",
    "asdfljhbb",
    "=b"
])
def test_200_vote(vote):
    payload = "vote=" + vote
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.request("POST", VOTER_URL, headers=headers, data=payload)
    assert response.status_code == 200
    assert "voter_id" in response.headers.get('Set-Cookie')
    assert response.headers.get("Connection") == "close"
    assert response.headers.get("Content-Type") == "text/html; charset=utf-8"


@pytest.mark.parametrize("bad_payload", [
    "votes=a",
    "",
    "0"
])
def test_400_response(bad_payload):
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.request("POST", VOTER_URL, headers=headers, data=bad_payload)
    assert response.status_code == 400
    assert response.headers.get("Connection") == "close"
    assert response.headers.get("Content-Type") == "text/html"
