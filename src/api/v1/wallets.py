import logging
from typing import Annotated

from tronpy import AsyncTron
from tronpy.exceptions import AddressNotFound

from core.dependencies.helper import db_helper


from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from core.dependencies.tron import get_tron_client
from core.schemas import WalletSchema
from services.wallets import write_wallet_data

router = APIRouter(tags=["Wallets"])

log = logging.getLogger(__name__)


@router.post(
    "/{address}",
    response_model=WalletSchema,
)
async def send_wallet_information(
    address: str,
    session: Annotated[
        AsyncSession,
        Depends(db_helper.get_async_session_with_commit),
    ],
    tron_client: Annotated[
        AsyncTron,
        Depends(get_tron_client),
    ],
):
    try:
        return await write_wallet_data(
            session=session, tron_client=tron_client, address=address
        )

    except (ValueError, AddressNotFound):
        log.exception(
            "Не удалось получить информацию о кошельке %r", address
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Address not found or invalid.",
        )
