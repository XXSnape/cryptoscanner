from fastapi import Request
from tronpy import AsyncTron


def get_tron_client(
    request: Request,
) -> AsyncTron:
    """
    Возвращает клиент Tron для асинхронного взаимодействия с приложением.
    """
    return request.app.state.tron_client
