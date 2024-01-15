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
