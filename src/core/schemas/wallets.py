from decimal import Decimal

from pydantic import BaseModel
from datetime import datetime


class WalletSchema(BaseModel):
    address: str
    balance_trx: Decimal
    bandwidth: int
    energy: int
    date_and_time: datetime | None = None


class WalletsInfoSchema(BaseModel):
    items: list[WalletSchema]
    total_count: int
    page: int
    pages: int
