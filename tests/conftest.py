from collections.abc import AsyncGenerator
from decimal import Decimal
from os import getenv
from pathlib import Path

import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)
from tronpy import AsyncTron
from tronpy.providers import AsyncHTTPProvider

from core.dependencies.helper import db_helper
from core.dependencies.tron import get_tron_client
from core.models import Base, Wallet
from src.main import main_app

DIR = Path(__file__).resolve().parent
engine = create_async_engine(
    f"sqlite+aiosqlite:///{DIR}/test_db.sqlite3", poolclass=NullPool
)
async_session_maker = async_sessionmaker(
    engine, expire_on_commit=False, autoflush=False
)
FAKE_WALLET = "TULkcTBMUfxuXcmVMG6LVY6KQfiwtjH5E6"


@pytest.fixture(scope="session", autouse=True)
def check_env() -> None:
    """
    Проверяет наличие переменных окружения TEST_WALLET и API_KEY в файле .env.
    """
    if not getenv("TEST_WALLET") or not getenv("API_KEY"):
        pytest.exit(
            "Для тестов в файл .env необходимо указать TEST_WALLET и API_KEY",
        )


@pytest.fixture
def real_wallet_address() -> str:
    """
    Возвращает адрес кошелька для тестов.
    """
    return getenv("TEST_WALLET")


@pytest.fixture(scope="session", autouse=True)
async def init_db():
    """
    Инициализация тестовой базы данных перед запуском тестов
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    async with async_session_maker() as session:
        wallets = [
            Wallet(
                address=FAKE_WALLET,
                balance_trx=Decimal("138.621687"),
                bandwidth=67_227,
                energy=1_170_559,
            ),
            Wallet(
                address=FAKE_WALLET,
                balance_trx=Decimal("60.957124"),
                bandwidth=271,
                energy=0,
            ),
            Wallet(
                address=FAKE_WALLET,
                balance_trx=Decimal("0.000001"),
                bandwidth=600,
                energy=0,
            ),
            Wallet(
                address=FAKE_WALLET,
                balance_trx=Decimal("2401.723903"),
                bandwidth=3_052_336,
                energy=218_977_380,
            ),
        ]
        session.add_all(wallets)
        await session.commit()


@pytest.fixture()
async def async_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Генерирует сессию для асинхронного взаимодействия с тестовой базой данных внутри тестов.
    """
    async with async_session_maker() as session:  # type: AsyncSession
        yield session


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    """
    Возвращает клиента для асинхронного взаимодействия с приложением внутри тестов.
    """

    async with AsyncClient(
        transport=ASGITransport(app=main_app),
        base_url="http://test/api/v1/",
    ) as ac:
        yield ac


async def override_get_async_session_without_commit() -> (
    AsyncGenerator[AsyncSession, None]
):
    """
    Генерирует сессию для асинхронного взаимодействия
    с тестовой базой данных внутри приложения без коммита.
    """
    async with async_session_maker() as session:  # type: AsyncSession
        yield session


async def override_get_async_session_with_commit() -> (
    AsyncGenerator[AsyncSession, None]
):
    """
    Генерирует сессию для асинхронного взаимодействия
    с тестовой базой данных внутри приложения c коммитом.
    """
    async with async_session_maker() as session:  # type: AsyncSession
        yield session
        await session.commit()


async def override_get_tron_client() -> AsyncGenerator:
    """
    Генерирует клиент Tron для асинхронного взаимодействия с тестовой базой данных внутри приложения.
    """
    async with AsyncTron(
        AsyncHTTPProvider(api_key=getenv("API_KEY"))
    ) as tron_client:
        yield tron_client


main_app.dependency_overrides[
    db_helper.get_async_session_without_commit
] = override_get_async_session_without_commit
main_app.dependency_overrides[
    db_helper.get_async_session_with_commit
] = override_get_async_session_with_commit

main_app.dependency_overrides[get_tron_client] = (
    override_get_tron_client
)
