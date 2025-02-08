import yaml
import pytest
from playwright.sync_api import sync_playwright

# Load YAML config
with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)

@pytest.fixture
def api_request():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context()
        request = context.request
        yield request
        browser.close()

def test_api_login(api_request):
    response = api_request.post(
        f"{config['base_url']}{config['api']['login']}",
        data={"email": "eve.holt@reqres.in", "password": "cityslicka"}
    )
    assert response.status == 200
    json_data = response.json()
    assert "token" in json_data

def test_get_users(api_request):
    response = api_request.get(f"{config['base_url']}{config['api']['users']}")
    assert response.status == 200
    assert len(response.json()["data"]) > 0

def test_create_user(api_request):
    response = api_request.post(
        f"{config['base_url']}{config['api']['create_user']}",
        data={"name": "John Doe", "job": "QA Engineer"}
    )
    assert response.status == 201
    json_data = response.json()
    assert json_data["name"] == "John Doe"
