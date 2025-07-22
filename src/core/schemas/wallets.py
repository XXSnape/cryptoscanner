from decimal import Decimal

from pydantic import BaseModel


class WalletSchema(BaseModel):
    address: str
    balance_trx: Decimal
    bandwidth: int
    energy: int
