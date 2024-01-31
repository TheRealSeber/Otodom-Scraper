from enum import Enum


class OfferedBy(Enum):
    PRIVATE = "private"
    ESTATE_AGENCY = "agency"


class AuctionType(Enum):
    SALE = "sale"
    RENT = "rent"


class PropertyType(Enum):
    FLAT = "flat"
    STUDIO = "studio"
    HOUSE = "house"
    INVESTMENT = "investment"
    ROOM = "room"
    PLOT = "plot"
    VENUE = "venue"
    MAGAZINE = "magazine"
    GARAGE = "garage"


class ConstructionStatus(Enum):
    TO_RENOVATE = "to_renovate"
    TO_FINISH = "to_completion"
    READY_TO_USE = "ready_to_use"


class MarketType(Enum):
    PRIMARY = "primary"
    SECONDARY = "secondary"


class Constans:
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

    CSV_KEYS = [
        "_id",
        "agency__id",
        "agency_city",
        "agency_county",
        "agency_name",
        "agency_otodom_id",
        "agency_postal_code",
        "agency_province",
        "agency_street",
        "area",
        "auction_type",
        "building_build_year",
        "building_floors",
        "building_type",
        "created_at",
        "estate_agency",
        "extras",
        "floor",
        "heating",
        "link",
        "localization_city",
        "localization_county",
        "localization_district",
        "localization_latitude",
        "localization_longitude",
        "localization_province",
        "localization_street",
        "market_type",
        "offered_by",
        "otodom_id",
        "price",
        "price_per_meter",
        "promoted",
        "property_type",
        "rent",
        "rooms",
        "security_types",
        "title",
    ]


AUCTION_TYPE_MAP = {
    "sprzedaz": AuctionType.SALE,
    "wynajem": AuctionType.RENT,
}

PROPERTY_TYPE_MAP = {
    "mieszkanie": PropertyType.FLAT,
    "kawalerka": PropertyType.STUDIO,
    "dom": PropertyType.HOUSE,
    "inwestycja": PropertyType.INVESTMENT,
    "pokoj": PropertyType.ROOM,
    "dzialka": PropertyType.PLOT,
    "lokal": PropertyType.VENUE,
    "haleimagazyny": PropertyType.MAGAZINE,
    "garaz": PropertyType.GARAGE,
}
