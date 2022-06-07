import pytest
import requests
import json
import logging
					
RESULT_URL = "http://localhost:9876/socket.io/?transport=polling"


def strip_string(s):
    try:
        s = s[:0] + s[4:]
        s = s[:-4]
        return s
    except:
        return ""


def response_to_json(response):
    try:
        s = strip_string(response.text)
        return json.loads(s)
    except:
        logging.error("Couldn't process response. Returning empty json...")
        return json.loads("{}")


@pytest.fixture
def get_sid():
    response = requests.request("GET", RESULT_URL)
    response_json = response_to_json(response)
    return response_json.get("sid")


def test_no_sid_200_response():
    response = requests.request("GET", RESULT_URL)
    response_json = response_to_json(response)
    assert response.status_code == 200
    assert response.headers.get("Connection") == "keep-alive"
    assert response.headers.get("Content-Type") == "text/plain; charset=UTF-8"
    assert "sid" in response_json
    assert "pingInterval" in response_json
    assert "pingTimeout" in response_json
    assert "upgrades" in response_json


def test_sid_200_response(get_sid):
    response = requests.request("GET", RESULT_URL + "&sid=" + get_sid)
    assert response.status_code == 200
    assert "message" in response.text
    assert '{"text":"Welcome!"}' in response.text


@pytest.mark.parametrize("bad_id", [
    "gg",
    "-1",
    "0"
])
def test_bad_sid_400_response(bad_id):
    response = requests.request("GET", RESULT_URL + "&sid=" + bad_id)
    assert response.status_code == 400
    assert response.headers.get("Connection") == "keep-alive"
    assert response.headers.get("Content-Type") == "application/json"
    assert response.json().get("code") == 1
    assert response.json().get("message") == "Session ID unknown"


def test_no_transport_400_response():
    response = requests.request("GET", "http://localhost:9876/socket.io/")
    assert response.status_code == 400
    assert response.headers.get("Connection") == "keep-alive"
    assert response.headers.get("Content-Type") == "application/json"
    assert response.json().get("code") == 0
    assert response.json().get("message") == "Transport unknown"
