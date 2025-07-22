from datetime import datetime
from decimal import Decimal

from sqlalchemy import Numeric, func
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Wallet(Base):
    """
    Модель для хранения информации о кошельке Tron.
    """

    address: Mapped[str]
    balance_trx: Mapped[Decimal] = mapped_column(
        Numeric(
            scale=6,
            decimal_return_scale=6,
        )
    )
    bandwidth: Mapped[int]
    energy: Mapped[int]
    date_and_time: Mapped[datetime] = mapped_column(
        default=datetime.now,
        server_default=func.now(),
    )
