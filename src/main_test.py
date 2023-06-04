import pytest
from sanic_testing.testing import SanicTestClient

from src.main import app


@pytest.fixture
def client() -> SanicTestClient:
    client = SanicTestClient(app)
    return client


def test_healthcheck(client: SanicTestClient):
    _, response = client.get("/healthcheck")
    assert response.status == 200


def test_get_report(client: SanicTestClient):
    _, response = client.get("/report")
    assert response.status == 200

    _, response = client.get("/report?date_from=03.02.2021")
    assert response.status == 200

    _, response = client.get("/report?date_from=03.02.2021&date_to=04.02.2021")
    assert response.status == 200

    _, response = client.get("/report?date_from=03.02.2021&date_to=04.02.2021&position=1")
    assert response.status == 200

    _, response = client.get("/report?date_from=03.02.2021&date_to=04.02.2021&position=1&position=2")
    assert response.status == 200

    _, response = client.get(
        "/report?date_from=03.02.2021&date_to=04.02.2021&position=1&position=2&level=внутривузовские"
    )
    assert response.status == 200
