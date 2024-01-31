import json

from mongoengine import connect as mongo_connect


def connect_to_database(host: str = None) -> None:
    """
    Connect to the database.

    If host is None then tries to connect to the database
    with the url defined in settings.json.

    :param host: The host of the database
    """
    if host is None:
        with open("settings.json", "r", encoding="utf-8") as f:
            settings = json.load(f)
            host = settings["database"]["host"]
            if not host:
                raise ValueError("Database host is not defined in settings.json")
    mongo_connect(host=host)
