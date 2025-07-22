def clean_date(
    response: dict[str, str | int | list],
) -> dict[str, int | list[str | int]]:
    for obj in response["items"]:
        obj.pop("date_and_time")
    return response
