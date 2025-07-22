def clean_date(
    response: dict[str, str | int | list],
) -> dict[str, int | list[str | int]]:
    """
    Очистка даты и времени из ответа API.
    """
    for obj in response["items"]:
        obj.pop("date_and_time")
    return response
