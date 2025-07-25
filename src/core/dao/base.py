import logging

from pydantic import BaseModel
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Base

logger = logging.getLogger(__name__)


class BaseDAO[M: Base]:
    """
    Базовый класс DAO для работы с моделями SQLAlchemy.
    """

    model: type[M] | None = None

    def __init__(self, session: AsyncSession):
        """
        Инициализация DAO сессией SQLAlchemy.
        """
        self._session = session
        if self.model is None:
            raise ValueError(
                "Модель должна быть указана в дочернем классе"
            )

    async def add(self, values: BaseModel) -> M:
        """
        Добавляет новую запись в базу данных.
        """
        values_dict = values.model_dump(exclude_unset=True)
        logger.info(
            "Добавление записи %s с параметрами: %s",
            self.model.__name__,
            values_dict,
        )
        try:
            new_instance = self.model(**values_dict)
            self._session.add(new_instance)
            await self._session.flush()
            logger.info(
                "Запись %s успешно добавлена.", self.model.__name__
            )
            return new_instance
        except SQLAlchemyError as e:
            await self._session.rollback()
            logger.error("Ошибка при добавлении записи %s", e)
            raise
