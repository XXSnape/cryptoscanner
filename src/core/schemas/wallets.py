from decimal import Decimal
from typing import Annotated

from pydantic import BaseModel, Field
from datetime import datetime


class WalletSchema(BaseModel):
    address: str
    balance_trx: Annotated[Decimal, Field(decimal_places=6)]
    bandwidth: int
    energy: int
    date_and_time: datetime | None = None


class WalletsInfoSchema(BaseModel):
    items: list[WalletSchema]
    total_count: int
    page: int
    pages: int
