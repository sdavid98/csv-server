import pytest
from server import app as api


@pytest.fixture()
def app():
    yield api


@pytest.fixture()
def client(app):
    return app.test_client()


def test_no_resource_given(client):
    response = client.get("/")
    assert response.status_code == 404


def test_resource_not_found(client):
    response = client.get("/non-existant-filename")
    assert response.status_code == 404


def test_resource_returns_whole_json(client):
    response = client.get("/amp_organization_applications")
    assert response.status_code == 200
    first_element = response.json[0]
    assert first_element == {
        "organizationId": 2146948263,
        "applicationKey": "actions-activate-feature|1.0.0"
    }
    assert len(response.json) == 66


def test_resource_returns_partial_json(client):
    response = client.get("/amp_organization_applications?limit=2&offset=2")
    assert response.json == [
        {
            "organizationId": 2146948263,
            "applicationKey": "actions-agent-management|1.7.0"
        },
        {
            "organizationId": 2146948263,
            "applicationKey": "backstage-actions-admin|2.4.0-SNAPSHOT"
        }
    ]
