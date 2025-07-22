import asyncio

from sqlalchemy.ext.asyncio import AsyncSession
from tronpy import AsyncTron

from core.dao.wallet import WalletDao
from core.schemas import WalletSchema
from core.schemas.wallets import WalletsInfoSchema


async def write_wallet_data(
    session: AsyncSession,
    tron_client: AsyncTron,
    address: str,
) -> WalletSchema:

    balance_trx, bandwidth, energy = await asyncio.gather(
        tron_client.get_account_balance(address),
        tron_client.get_bandwidth(address),
        tron_client.get_energy(address),
    )
    wallet = WalletSchema(
        address=address,
        balance_trx=balance_trx,
        bandwidth=bandwidth,
        energy=energy,
    )
    result = await WalletDao(session=session).add(wallet)
    wallet.date_and_time = result.date_and_time
    return wallet


async def get_wallet_data(
    session: AsyncSession,
    address: str,
    page: int,
    per_page: int,
) -> WalletsInfoSchema:
    items, total_count = await WalletDao(
        session=session
    ).get_paginated_data(
        session=session,
        address=address,
        page=page,
        per_page=per_page,
    )
    return WalletsInfoSchema(
        total_count=total_count,
        items=[
            WalletSchema.model_validate(item, from_attributes=True)
            for item in items
        ],
        page=page,
        pages=(total_count + per_page - 1) // per_page,
    )
