import asyncio

from sqlalchemy.ext.asyncio import AsyncSession
from tronpy import AsyncTron

from core.dao.wallet import WalletDao
from core.schemas import WalletSchema


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
    await WalletDao(session=session).add(wallet)
    return wallet
