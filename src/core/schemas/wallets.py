from decimal import Decimal
from typing import Annotated

from pydantic import BaseModel, Field
from datetime import datetime


class WalletSchema(BaseModel):
    """
    Схема для представления информации о кошельке Tron.
    """
    address: str
    balance_trx: Annotated[Decimal, Field(decimal_places=6)]
    bandwidth: int
    energy: int
    date_and_time: datetime | None = None


class WalletsInfoSchema(BaseModel):
    """
    Схема для представления информации о кошельке за разные промежутки времени с пагинацией.
    """
    items: list[WalletSchema]
    total_count: int
    page: int
    pages: int
