import httpx

from api.services.http_client import HttpClient


def _client(handler, sleeps: list[float]) -> HttpClient:
    return HttpClient(
        timeout_seconds=5,
        max_retries=3,
        backoff_seconds=0.5,
        backoff_max_seconds=8,
        client=httpx.Client(transport=httpx.MockTransport(handler)),
        sleep=sleeps.append,
    )


def test_post_timeout_then_success_uses_exponential_backoff() -> None:
    calls = {"count": 0}

    def handler(request: httpx.Request) -> httpx.Response:
        calls["count"] += 1
        if calls["count"] == 1:
            raise httpx.TimeoutException("timeout")
        return httpx.Response(200, headers={"Retry-After": "9"})

    sleeps: list[float] = []
    response = _client(handler, sleeps).post(
        "https://example.com", {"content": "Hello world"}
    )

    assert response.status_code == 200
    assert sleeps == [0.5]


def test_get_retries_on_503() -> None:
    calls = {"count": 0}

    def handler(request: httpx.Request) -> httpx.Response:
        calls["count"] += 1
        if calls["count"] == 1:
            return httpx.Response(503)
        return httpx.Response(200)

    sleeps: list[float] = []
    response = _client(handler, sleeps).get("https://example.com/accounts/1")

    assert response.status_code == 200
    assert sleeps == [0.5]


def test_get_passes_headers() -> None:
    seen: dict[str, str] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        seen["authorization"] = request.headers.get("Authorization", "")
        return httpx.Response(200)

    _client(handler, []).get(
        "https://example.com/accounts/1",
        headers={"Authorization": "Bearer token"},
    )

    assert seen["authorization"] == "Bearer token"
