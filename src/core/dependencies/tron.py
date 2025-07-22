from fastapi import Request
from tronpy import AsyncTron


def get_tron_client(
    request: Request,
) -> AsyncTron:
    return request.app.state.tron_client
