import time
from collections.abc import Callable

import httpx

_RETRY_STATUSES = {429, 500, 502, 503, 504}


class HttpClient:
    def __init__(
        self,
        timeout_seconds: float,
        max_retries: int,
        backoff_seconds: float,
        backoff_max_seconds: float,
        client: httpx.Client | None = None,
        sleep: Callable[[float], None] = time.sleep,
    ) -> None:
        self._max_retries = max_retries
        self._backoff_seconds = backoff_seconds
        self._backoff_max_seconds = backoff_max_seconds
        self._client = client or httpx.Client(timeout=httpx.Timeout(timeout_seconds))
        self._sleep = sleep

    def get(self, url: str, headers: dict[str, str] | None = None) -> httpx.Response:
        return self._request("GET", url, headers=headers)

    def post(
        self,
        url: str,
        json: dict,
        headers: dict[str, str] | None = None,
    ) -> httpx.Response:
        return self._request("POST", url, json=json, headers=headers)

    def _request(
        self,
        method: str,
        url: str,
        json: dict | None = None,
        headers: dict[str, str] | None = None,
    ) -> httpx.Response:
        attempt = 0
        while True:
            try:
                response = self._client.request(method, url, json=json, headers=headers)
            except (httpx.TimeoutException, httpx.ConnectError):
                if attempt >= self._max_retries:
                    raise
                self._sleep(self._backoff(attempt))
                attempt += 1
                continue

            if response.status_code not in _RETRY_STATUSES or attempt >= self._max_retries:
                return response

            self._sleep(self._wait(response, attempt))
            attempt += 1

    def _backoff(self, attempt: int) -> float:
        return min(self._backoff_seconds * (2**attempt), self._backoff_max_seconds)

    def _wait(self, response: httpx.Response, attempt: int) -> float:
        if response.status_code != 429:
            return self._backoff(attempt)
        retry_after = response.headers.get("Retry-After")
        if retry_after is None:
            return self._backoff(attempt)
        try:
            seconds = float(retry_after)
        except ValueError:
            return self._backoff(attempt)
        return min(seconds, self._backoff_max_seconds)
