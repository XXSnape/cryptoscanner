from core.config import settings
from fastapi import APIRouter

from .v1 import router as wallets_api_v1

router = APIRouter(
    prefix=settings.api.prefix,
)
router.include_router(wallets_api_v1)
