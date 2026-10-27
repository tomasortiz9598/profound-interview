from api.schemas import AccountChallengeStarted
from api.tasks import run_account_challenge
from fastapi import APIRouter

router = APIRouter(prefix="/account-challenge", tags=["account_challenge"])


@router.post("", response_model=AccountChallengeStarted)
async def start_account_challenge() -> AccountChallengeStarted:
    run_account_challenge.delay()
    return AccountChallengeStarted(status="queued")
