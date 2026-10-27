from unittest.mock import patch

from api.main import app
from fastapi.testclient import TestClient


def test_start_account_challenge_queues_task() -> None:
    client = TestClient(app)
    with patch("api.routers.account_challenge_router.run_account_challenge.delay") as delay:
        response = client.post("/account-challenge")

    delay.assert_called_once_with()
    assert response.status_code == 200
    assert response.json() == {"status": "queued"}
