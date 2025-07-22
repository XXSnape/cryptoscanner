import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from tronpy import AsyncTron
from tronpy.exceptions import AddressNotFound

from core.dependencies.helper import db_helper
from core.dependencies.tron import get_tron_client
from core.schemas import WalletSchema
from core.schemas.wallets import WalletsInfoSchema
from services.wallets import get_wallet_data, write_wallet_data

router = APIRouter(tags=["Wallets"])

log = logging.getLogger(__name__)


@router.post(
    "/{address}",
    response_model=WalletSchema,
    status_code=status.HTTP_201_CREATED,
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
    """
    Получает информацию о кошельке и сохраняет её в базу данных.
    """
    try:
        return await write_wallet_data(
            session=session, tron_client=tron_client, address=address
        )

    except (ValueError, AddressNotFound):
        log.error(
            "Не удалось получить информацию о кошельке %r", address
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Address not found or invalid.",
        )
    except Exception:
        log.exception(
            "Не удалось получить информацию о кошельке %r по внутренней ошибке",
            address,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="INTERNAL SERVER ERROR.",
        )


@router.get(
    "/{address}",
    response_model=WalletsInfoSchema,
)
async def get_wallet_information(
    address: str,
    session: Annotated[
        AsyncSession,
        Depends(db_helper.get_async_session_without_commit),
    ],
    page: Annotated[
        int,
        Query(
            ge=1,
            le=1_000_000,
            description="Страница для пагинации (начиная с 1)",
        ),
    ] = 1,
    per_page: Annotated[
        int,
        Query(
            ge=1,
            le=100,
            description="Количество записей на странице (макс. 100)",
        ),
    ] = 10,
):
    """
    Получает информацию о кошельке с пагинацией.
    """
    return await get_wallet_data(
        session=session,
        address=address,
        page=page,
        per_page=per_page,
    )
