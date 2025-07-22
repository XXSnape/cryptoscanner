from decimal import Decimal

import httpx
import pytest
from httpx import AsyncClient
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from core.dao.wallet import WalletDao
from core.models import Wallet
from core.schemas import WalletSchema
from tests.conftest import FAKE_WALLET, async_session_maker
from tests.utils import clean_date


@pytest.mark.parametrize(
    "page, per_page, expected",
    (
        (
            None,
            None,
            {
                "items": [
                    {
                        "address": "TULkcTBMUfxuXcmVMG6LVY6KQfiwtjH5E6",
                        "balance_trx": "138.621687",
                        "bandwidth": 67227,
                        "energy": 1170559,
                    },
                    {
                        "address": "TULkcTBMUfxuXcmVMG6LVY6KQfiwtjH5E6",
                        "balance_trx": "60.957124",
                        "bandwidth": 271,
                        "energy": 0,
                    },
                    {
                        "address": "TULkcTBMUfxuXcmVMG6LVY6KQfiwtjH5E6",
                        "balance_trx": "0.000001",
                        "bandwidth": 600,
                        "energy": 0,
                    },
                    {
                        "address": "TULkcTBMUfxuXcmVMG6LVY6KQfiwtjH5E6",
                        "balance_trx": "2401.723903",
                        "bandwidth": 3052336,
                        "energy": 218977380,
                    },
                ],
                "total_count": 4,
                "page": 1,
                "pages": 1,
            },
        ),
        (
            1,
            2,
            {
                "items": [
                    {
                        "address": "TULkcTBMUfxuXcmVMG6LVY6KQfiwtjH5E6",
                        "balance_trx": "138.621687",
                        "bandwidth": 67227,
                        "energy": 1170559,
                    },
                    {
                        "address": "TULkcTBMUfxuXcmVMG6LVY6KQfiwtjH5E6",
                        "balance_trx": "60.957124",
                        "bandwidth": 271,
                        "energy": 0,
                    },
                ],
                "total_count": 4,
                "page": 1,
                "pages": 2,
            },
        ),
        (
            2,
            2,
            {
                "items": [
                    {
                        "address": "TULkcTBMUfxuXcmVMG6LVY6KQfiwtjH5E6",
                        "balance_trx": "0.000001",
                        "bandwidth": 600,
                        "energy": 0,
                    },
                    {
                        "address": "TULkcTBMUfxuXcmVMG6LVY6KQfiwtjH5E6",
                        "balance_trx": "2401.723903",
                        "bandwidth": 3052336,
                        "energy": 218977380,
                    },
                ],
                "total_count": 4,
                "page": 2,
                "pages": 2,
            },
        ),
        (
            3,
            2,
            {
                "items": [],
                "total_count": 4,
                "page": 3,
                "pages": 2,
            },
        ),
    ),
)
async def test_get_wallet_with_pagination(
    ac: AsyncClient,
    page: int | None,
    per_page: int | None,
    expected: dict,
) -> None:
    """
    Тестирование получения информации о кошельке с пагинацией.
    """
    params = (
        {
            "page": page,
            "per_page": per_page,
        }
        if page
        else None
    )

    response = await ac.get(f"wallets/{FAKE_WALLET}", params=params)
    assert response.status_code == httpx.codes.OK
    assert clean_date(response.json()) == expected


async def test_write_wallet_data(
    async_session: AsyncSession,
) -> None:
    """
    Тестирование записи данных о кошельке в базу данных.
    """
    address = "TQguVRm3tDmZG7AeZ47Mk6qi6GTF1ZDqkZ"
    dao = WalletDao(session=async_session)
    await dao.add(
        WalletSchema(
            address=address,
            balance_trx=Decimal("234.00001"),
            bandwidth=321,
            energy=150,
        ),
    )
    await async_session.commit()
    q = select(func.count()).where(Wallet.address == address)
    assert (await async_session.execute(q)).scalar_one() == 1
