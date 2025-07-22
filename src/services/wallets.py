import asyncio

from tronpy import AsyncTron
from core.schemas import WalletSchema


async def get_wallet_data(
    tron_client: AsyncTron,
    address: str,
) -> WalletSchema:

    balance_trx, bandwidth, energy = await asyncio.gather(
        tron_client.get_account_balance(address),
        tron_client.get_bandwidth(address),
        tron_client.get_energy(address),
    )
    return WalletSchema(
        address=address,
        balance_trx=balance_trx,
        bandwidth=bandwidth,
        energy=energy,
    )
