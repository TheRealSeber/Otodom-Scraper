from enum import Enum


class PropertyType(Enum):
    FLAT = "mieszkanie"
    STUDIO = "kawalerka"
    HOUSE = "dom"
    INVESTMENT = "inwestycja"
    ROOM = "pokoj"
    PLOT = "dzialka"
    VENUE = "lokal"
    MAGAZINE = "haleimagazyny"
    GARAGE = "garaz"


class AuctionType(Enum):
    SALE = "sprzedaz"
    RENT = "wynajem"


class Defaults:
    """
    A class that provides default values for the settings used by the application.

    Attributes:
        DEFAULT_URL (str): The default base URL for the Otodom website.
        DEFAULT_PRICE_MIN (int): The default minimum price for the property.
        DEFAULT_PRICE_MAX (int): The default maximum price for the property.
        DEFAULT_PROVINCE (str): The default province where the property is located.
        DEFAULT_CITY (str): The default city where the property is located.
        DEFAULT_DISTRICT (str, optional): The default district of the city.
        Defaults to `None`.
        DEFAULT_PROPERTY_TYPE (str): The default type of property.
        DEFAULT_AUCTION_TYPE (str): The default type of auction.
    """

    DEFAULT_URL = "https://www.otodom.pl"
    DEFAULT_PRICE_MIN = 0
    DEFAULT_PRICE_MAX = 10000000
    DEFAULT_PROVINCE = "mazowieckie"
    DEFAULT_CITY = "warszawa"
    DEFAULT_DISTRICT = None
    DEFAULT_PROPERTY_TYPE = PropertyType.FLAT
    DEFAULT_AUCTION_TYPE = AuctionType.SALE
