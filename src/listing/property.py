import json
from datetime import datetime
from enum import Enum

from bs4 import ResultSet
from common import AUCTION_TYPE_MAP
from common import AuctionType
from common import Constans
from common import ConstructionStatus
from common import MarketType
from common import OfferedBy
from common import PROPERTY_TYPE_MAP
from common import PropertyType
from listing.building import Building
from listing.localization import Localization


class Property:
    """
    A class that represents a property on the otodom.pl website.
    """

    def __init__(self, code: ResultSet):
        """
        Initializes the Prop instance.

        Some of the attributes has defined types and during extraction of the data,
        they a guarantee to exist, but for the sake of the initialization
        they are set to None for now.

        :param code: The HTML code of the listing page
        """
        self.link: str = Constans.DEFAULT_URL + self.extract_link(code)
        self.promoted: bool = self.extract_promoted(code)
        self.created_at: datetime = None
        self.otodom_id: int = None
        self.title: str = None
        self.area: int = None
        self.floor: int | None = None
        self.price: int | None = None
        self.price_per_meter: float | None = None
        self.rooms: int | None = None
        self.rent: int | None = None
        self.heating: str | None = None
        self.extras: str | None = None
        self.security_types: list[str] | None = None
        self.offered_by: str | None = None
        self.property_type: PropertyType = None
        self.market_type: MarketType = None
        self.auction_type: AuctionType = None
        self.localization: Localization = None
        self.construction_status: ConstructionStatus | None = None
        self.building: Building | None = None

    @staticmethod
    def extract_link(code: ResultSet) -> str:
        """
        Extracts the link from the HTML code.

        :param code: The HTML code containing the link
        :return: The extracted link
        """
        return code.select_one("a")["href"]

    @staticmethod
    def extract_promoted(code: ResultSet) -> bool:
        """
        Determines whether the property is promoted on the page.

        :param code: The HTML code containing the promotion status
        :return: True if the property is promoted on the page, False otherwise
        """
        return code.select_one("article>span+div") is not None

    @staticmethod
    def extract_construction_status(properties: dict) -> ConstructionStatus | None:
        """
        Determines the construction status from the properties.

        :param properties: The properties containing the construction status
        :return: The construction status
        """
        if properties.get("ConstructionStatus") is None:
            return None
        return ConstructionStatus(properties["ConstructionStatus"])

    @staticmethod
    def extract_building(properties: dict) -> Building | None:
        """
        Determines the building from the properties.

        :param properties: The properties containing the building
        :return: The building
        """
        if (
            properties.get("Building_floors_num") is None
            and properties.get("Building_type") is None
            and properties.get("Build_year") is None
        ):
            return None
        return Building(properties)

    @staticmethod
    def extract_offered_by(properties: dict) -> str:
        """
        Determines the offer type from the properties.

        :param properties: The properties containing the offer type
        :return: The offer type
        """
        return (
            OfferedBy.PRIVATE
            if properties["agency"] is None
            else OfferedBy.ESTATE_AGENCY
        )

    @staticmethod
    def informational_json_exists(code: ResultSet) -> bool:
        """
        Checks if the JSON with informations about the property
        in the returned data from the request is available.

        :param code: The HTML code of the property page
        :return: True if the JSON with the property informations exists int the code,
            False otherwise
        """
        return code.find("script", {"type": "application/json"}) is not None

    @staticmethod
    def extract_property_floor(properties: dict) -> str | None:
        """
        Extracts the floor of the property from the properties.

        :param properties: The properties containing the floor of the property
        :return: The floor of the property
        """
        floor = properties.get("Floor_no")
        if floor is None:
            return None
        res = ""
        for f in floor:
            if "ground" in f:
                res += "0" + ","
            elif "higher_" in f:
                res += "<" + f.split("_")[-1] + ","
            elif "_" in f:
                res += f.split("_")[-1] + ","
            else:
                res += f + ","
        return res.removesuffix(",")

    @staticmethod
    def extract_extras(properties: dict) -> str | None:
        """
        Extracts the extras of the property from the properties.

        :param properties: The properties containing the extras of the property
        :return: The extras of the property
        """
        extras = properties.get("Extras_types")
        if extras is None:
            return None
        return ",".join(extras)

    @staticmethod
    def extract_created_at(properties: dict) -> datetime | None:
        """
        Extracts the creation date of the property from the properties.

        :param properties: The properties containing the creation date of the property
        :return: The creation date of the property
        """
        created_at = properties.get("createdAt")
        if created_at is None:
            return None
        return datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%S%z")

    @staticmethod
    def extract_rooms(properties: dict) -> str | None:
        """
        Extracts the number of rooms of the property from the properties.

        :param properties: The properties containing the number of rooms of the property
        :return: The number of rooms of the property
        """
        rooms = properties.get("Rooms_num")
        if rooms is None:
            return None
        return ",".join(rooms)

    @staticmethod
    def extract_heating(properties: dict) -> str | None:
        """
        Extracts the heating of the property from the properties.

        :param properties: The properties containing the heating of the property
        :return: The heating of the property
        """
        heating = properties.get("Heating")
        if heating is None:
            return None
        return ",".join(heating)

    @staticmethod
    def extract_security_types(properties: dict) -> str | None:
        """
        Extracts the security types of the property from the properties.

        :param properties: The properties containing the security types of the property
        :return: The security types of the property
        """
        security_types = properties.get("Security_types")
        if security_types is None:
            return None
        return ",".join(security_types)

    def extract_data_from_page(self, code: ResultSet) -> None:
        """
        Extracts data from the page and updates the property instance.

        This method loads the property information from a script tag in the HTML code,
        parses it as JSON and uses it to update the attributes of the property instance.

        :param code: The HTML code containing the property information
        """
        listing_information = json.loads(
            code.find("script", {"type": "application/json"}).text
        )
        listing_properties = listing_information["props"]["pageProps"]["ad"]
        self.otodom_id = listing_properties["id"]
        self.created_at = self.extract_created_at(listing_properties)
        self.title = listing_properties["title"]
        self.area = listing_properties["target"].get("Area", None)
        self.floor = self.extract_property_floor(listing_properties["target"])
        self.price = listing_properties["target"].get("Price", None)
        self.price_per_meter = listing_properties["target"].get("Price_per_m", None)
        self.rooms = self.extract_rooms(listing_properties["target"])
        self.rent = listing_properties["target"].get("Rent", None)
        self.heating = self.extract_heating(listing_properties["target"])
        self.extras = self.extract_extras(listing_properties["target"])
        self.security_types = self.extract_security_types(listing_properties["target"])
        self.property_type = PROPERTY_TYPE_MAP[
            listing_properties["target"]["ProperType"]
        ]
        self.market_type = MarketType(listing_properties["target"]["MarketType"])
        self.auction_type = AUCTION_TYPE_MAP[listing_properties["target"]["OfferType"]]
        self.localization = Localization(listing_properties["location"])
        self.construction_status = self.extract_construction_status(
            listing_properties["target"]
        )
        self.building = self.extract_building(listing_properties["target"])
        self.offered_by = self.extract_offered_by(listing_properties)

    def to_dict(self) -> dict:
        """
        Converts the Property instance to a dictionary.

        Removes all None values from the dictionary.

        :return: The Property representation as a dictionary
        """
        self_to_dict = {
            key: value for key, value in self.__dict__.items() if value is not None
        }
        enum_to_str = {
            key: val.value
            for key, val in self.__dict__.items()
            if isinstance(val, Enum)
        }
        self_to_dict.update(enum_to_str)
        if self.localization is not None:
            self_to_dict["localization"] = self.localization.to_dict()
        if self.building is not None:
            self_to_dict["building"] = self.building.to_dict()
        return self_to_dict
