from unittest.mock import MagicMock

import httpx
import pytest

from api.services.profound_account_service import ProfoundAccountService, ProfoundApiError


def _response(status_code: int, json_body: dict) -> httpx.Response:
    return httpx.Response(status_code, json=json_body)


def test_run_challenge_flow_calls_endpoints_in_order() -> None:
    http_client = MagicMock()
    account_id = "acct-1"
    http_client.post.side_effect = [
        _response(201, {"id": account_id, "name": "challenge-abc", "balance": 0}),
        _response(200, {"id": account_id, "name": "challenge-abc", "balance": 1000}),
        _response(200, {"id": account_id, "name": "challenge-abc", "balance": 500}),
    ]
    http_client.get.return_value = _response(
        200, {"id": account_id, "name": "challenge-abc", "balance": 0}
    )

    service = ProfoundAccountService(
        http_client=http_client,
        base_url="https://profound.build",
        bearer_token="secret",
    )
    result = service.run_challenge_flow("challenge-abc", 1000, 500)

    assert http_client.post.call_args_list[0].args == (
        "https://profound.build/v1/accounts",
        {"name": "challenge-abc"},
    )
    assert http_client.post.call_args_list[0].kwargs == {
        "headers": {"Authorization": "Bearer secret"}
    }
    http_client.get.assert_called_once_with(
        f"https://profound.build/v1/accounts/{account_id}",
        headers={"Authorization": "Bearer secret"},
    )
    assert http_client.post.call_args_list[1].args == (
        f"https://profound.build/v1/accounts/{account_id}/deposit",
        {"amount": 1000},
    )
    assert http_client.post.call_args_list[2].args == (
        f"https://profound.build/v1/accounts/{account_id}/withdraw",
        {"amount": 500},
    )
    assert result["after_withdraw"]["balance"] == 500


def test_run_challenge_flow_raises_on_withdraw_failure() -> None:
    http_client = MagicMock()
    account_id = "acct-1"
    http_client.post.side_effect = [
        _response(201, {"id": account_id, "name": "challenge-abc", "balance": 0}),
        _response(200, {"id": account_id, "name": "challenge-abc", "balance": 1000}),
        _response(400, {"detail": "insufficient funds"}),
    ]
    http_client.get.return_value = _response(
        200, {"id": account_id, "name": "challenge-abc", "balance": 0}
    )

    service = ProfoundAccountService(
        http_client=http_client,
        base_url="https://profound.build/",
        bearer_token="secret",
    )

    with pytest.raises(ProfoundApiError) as error:
        service.run_challenge_flow("challenge-abc", 1000, 500)

    assert error.value.status_code == 400
