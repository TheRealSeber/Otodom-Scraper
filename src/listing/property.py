import json
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
        self.otodom_id: int = None
        self.title: str = None
        self.area: int = None
        self.floor: int | None = None
        self.price: int | None = None
        self.price_per_meter: float | None = None
        self.rooms: int | None = None
        self.rent: int | None = None
        self.heating: str | None = None
        self.offered_by: str | None = None
        self.property_type: PropertyType = None
        self.market_type: MarketType = None
        self.auction_type: AuctionType = None
        self.localization: Localization = None
        self.construction_status: ConstructionStatus | None = None
        self.building: Building | None = None

    def __repr__(self) -> dict:
        return self.__dict__.__repr__()

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
        self.title = listing_properties["title"]
        self.area = listing_properties["target"].get("Area", None)
        self.floor = listing_properties["target"].get("Floor_no", [None])[0]
        self.price = listing_properties["target"].get("Price", None)
        self.price_per_meter = listing_properties["target"].get("Price_per_m", None)
        self.rooms = listing_properties["target"].get("Rooms_num", [None])[0]
        self.rent = listing_properties["target"].get("Rent", None)
        self.heating = listing_properties["target"].get("Heating", [None])[0]
        self.property_type = PROPERTY_TYPE_MAP[
            listing_properties["target"]["ProperType"]
        ]
        self.market_type = MarketType(listing_properties["target"]["MarketType"])
        self.auction_type = AUCTION_TYPE_MAP[listing_properties["target"]["OfferType"]]
        self.localization = Localization(listing_properties["location"]["address"])
        self.construction_status = self.extract_construction_status(
            listing_properties["target"]
        )
        self.building = self.extract_building(listing_properties["target"])
        self.offered_by = self.extract_offered_by(listing_properties)

    def to_dict(self):
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
