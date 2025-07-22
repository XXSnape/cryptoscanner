from typing import Sequence

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from .base import BaseDAO
from core.models import Wallet


class WalletDao(BaseDAO[Wallet]):
    model = Wallet

    async def get_paginated_data(
        self,
        session: AsyncSession,
        address: str,
        page: int,
        per_page: int,
    ) -> tuple[Sequence[Wallet], int]:
        count_query = select(func.count()).where(
            self.model.address == address
        )
        count_result = (
            await session.execute(count_query)
        ).scalar_one()
        query = (
            select(self.model)
            .where(self.model.address == address)
            .order_by(self.model.date_and_time.desc())
            .offset((page - 1) * per_page)
            .limit(per_page)
        )

        result = await session.execute(query)
        return result.scalars().all(), count_result
