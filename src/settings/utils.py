from settings.s_types import AuctionType
from settings.s_types import PropertyType

AUCTION_TYPE_MAPPING = {
    "sale": AuctionType.SALE,
    "rent": AuctionType.RENT,
}

PROPERTY_TYPE_MAPPING = {
    "flat": PropertyType.FLAT,
    "studio": PropertyType.STUDIO,
    "house": PropertyType.HOUSE,
    "investment": PropertyType.INVESTMENT,
    "room": PropertyType.ROOM,
    "plot": PropertyType.PLOT,
    "venue": PropertyType.VENUE,
    "magazine": PropertyType.MAGAZINE,
    "garage": PropertyType.GARAGE,
}

POLISH_CHARACTERS_MAPPING = {
    "ą": "a",
    "ć": "c",
    "ę": "e",
    "ł": "l",
    "ń": "n",
    "ó": "o",
    "ś": "s",
    "ź": "z",
    "ż": "z",
    "Ą": "A",
    "Ć": "C",
    "Ę": "E",
    "Ł": "L",
    "Ń": "N",
    "Ó": "O",
    "Ś": "S",
    "Ź": "Z",
    "Ż": "Z",
}


def get_auction_type(auction_type: str) -> AuctionType | None:
    """
    Get the AuctionType enum value corresponding to the given string.

    If the string does not match any of the keys in the AUCTION_TYPE_MAPPING dictionary,
    None is returned.

    :param auction_type: A string representing the auction type
    :return: The corresponding AuctionType enum value or None
    """
    return AUCTION_TYPE_MAPPING.get(auction_type.lower(), None)


def get_property_type(property_type: str) -> PropertyType | None:
    """
    Get the PropertyType enum value corresponding to the given string.

    If the string does not match any of the keys in the
    PROPERTY_TYPE_MAPPING dictionary, None is returned.

    :param property_type: A string representing the property type
    :return: The corresponding PropertyType enum value or None
    """
    return PROPERTY_TYPE_MAPPING.get(property_type.lower(), None)


def replace_polish_characters(text: str) -> str:
    """
    Replace Polish characters in the given text with their non-Polish equivalents.

    :param text: A string possibly containing text with Polish characters
    :return: The text with Polish characters replaced
    """
    return "".join([POLISH_CHARACTERS_MAPPING.get(c, c) for c in text])
