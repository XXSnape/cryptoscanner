from decimal import Decimal

from sqlalchemy import Numeric, func
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from .base import Base


class Wallet(Base):
    address: Mapped[str]
    balance_trx: Mapped[Decimal] = mapped_column(Numeric())
    bandwidth: Mapped[int]
    energy: Mapped[int]
    date_and_time: Mapped[datetime] = mapped_column(
        default=datetime.now,
        server_default=func.now(),
    )
