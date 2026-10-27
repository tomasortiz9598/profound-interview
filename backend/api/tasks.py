import uuid

from api.celery_app import celery_app
from api.services.http_client import HttpClient
from api.services.profound_account_service import ProfoundAccountService
from utils.settings import AppSettings

settings = AppSettings()


@celery_app.task
def run_account_challenge() -> None:
    http_client = HttpClient(
        timeout_seconds=settings.HTTP_TIMEOUT_SECONDS,
        max_retries=settings.HTTP_MAX_RETRIES,
        backoff_seconds=settings.HTTP_RETRY_BACKOFF_SECONDS,
        backoff_max_seconds=settings.HTTP_RETRY_BACKOFF_MAX_SECONDS,
    )
    service = ProfoundAccountService(
        http_client=http_client,
        base_url=settings.PROFOUND_API_BASE_URL,
        bearer_token=settings.PROFOUND_API_BEARER_TOKEN,
    )
    account_name = f"challenge-{uuid.uuid4().hex[:12]}"
    service.run_challenge_flow(account_name, deposit_cents=1000, withdraw_cents=500)
