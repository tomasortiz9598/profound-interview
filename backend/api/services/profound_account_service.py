from api.services.http_client import HttpClient


class ProfoundApiError(Exception):
    def __init__(self, status_code: int, url: str) -> None:
        self.status_code = status_code
        self.url = url
        super().__init__(f"Profound API returned {status_code} for {url}")


class ProfoundAccountService:
    def __init__(self, http_client: HttpClient, base_url: str, bearer_token: str) -> None:
        self._http_client = http_client
        self._base_url = base_url.rstrip("/")
        self._headers = {"Authorization": f"Bearer {bearer_token}"}

    def run_challenge_flow(
        self,
        account_name: str,
        deposit_cents: int,
        withdraw_cents: int,
    ) -> dict:
        created = self._create_account(account_name)
        account_id = created["id"]
        balance = self._get_account(account_id)
        deposited = self._deposit(account_id, deposit_cents)
        withdrawn = self._withdraw(account_id, withdraw_cents)
        return {
            "created": created,
            "balance_check": balance,
            "after_deposit": deposited,
            "after_withdraw": withdrawn,
        }

    def _create_account(self, name: str) -> dict:
        response = self._http_client.post(
            f"{self._base_url}/v1/accounts",
            {"name": name},
            headers=self._headers,
        )
        if response.status_code != 201:
            raise ProfoundApiError(response.status_code, f"{self._base_url}/v1/accounts")
        return response.json()

    def _get_account(self, account_id: str) -> dict:
        response = self._http_client.get(
            f"{self._base_url}/v1/accounts/{account_id}",
            headers=self._headers,
        )
        if response.status_code != 200:
            raise ProfoundApiError(
                response.status_code,
                f"{self._base_url}/v1/accounts/{account_id}",
            )
        return response.json()

    def _deposit(self, account_id: str, amount_cents: int) -> dict:
        url = f"{self._base_url}/v1/accounts/{account_id}/deposit"
        response = self._http_client.post(
            url,
            {"amount": amount_cents},
            headers=self._headers,
        )
        if response.status_code != 200:
            raise ProfoundApiError(response.status_code, url)
        return response.json()

    def _withdraw(self, account_id: str, amount_cents: int) -> dict:
        url = f"{self._base_url}/v1/accounts/{account_id}/withdraw"
        response = self._http_client.post(
            url,
            {"amount": amount_cents},
            headers=self._headers,
        )
        if response.status_code != 200:
            raise ProfoundApiError(response.status_code, url)
        return response.json()
