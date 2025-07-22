import httpx
from httpx import AsyncClient


async def test_send_and_get_wallet_information(
    ac: AsyncClient,
    real_wallet_address: str,
) -> None:
    """
    Тестирование отправки и получения информации о кошельке.
    """
    response = await ac.post(
        f"/wallets/{real_wallet_address}",
    )
    assert response.status_code == httpx.codes.CREATED
    json = response.json()
    assert "balance_trx" in json
    assert "bandwidth" in json
    assert "energy" in json
    assert "date_and_time" in json

    response = await ac.get(
        f"/wallets/{real_wallet_address}",
    )
    assert response.json() == {
        "items": [json],
        "total_count": 1,
        "page": 1,
        "pages": 1,
    }
    response = await ac.post(
        f"/wallets/abc",
    )
    assert response.status_code == httpx.codes.NOT_FOUND
    assert response.json() == {
        "detail": "Address not found or invalid."
    }
