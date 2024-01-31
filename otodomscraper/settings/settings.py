import json
import logging

from common import Constans
from settings.s_types import AuctionType
from settings.s_types import PropertyType
from settings.utils import AVAILABLE_PROVINCES
from settings.utils import get_auction_type
from settings.utils import get_property_type
from settings.utils import replace_polish_characters

logger = logging.getLogger(__name__)


class Settings:
    """
    This class represents the settings for a property search application.

    The settings include parameters such as the base URL for web scraping,
    price filters, selected province, city, district, and property type.

    Attributes:
        base_url (str): The base URL for web scraping.
        Defaults to the otodom.pl website.
        price_min (int): The minimum property price filter. Defaults to 0.
        price_max (int): The maximum property price filter. Defaults to 10,000,000.
        province (str): The selected province for property search.
        Defaults to "mazowieckie".
        city (str): The selected city for property search. Defaults to "warszawa".
        district (str): The selected district for property search. Defaults to None.
        property_type (str): The selected property type for filtering.
        Defaults to "mieszkanie".

    These default values are defined in the Defaults class.

    Example:
        To create a Settings object with default values:
        >>> settings = Settings()

        To access a specific setting:
        >>> print(settings.base_url)
        "https://www.otodom.pl"
    """

    def __init__(self):
        """
        Initialize the Settings object by loading the settings from a JSON file.

        If the file cannot be loaded, the settings are set to default values.
        """
        logger.info("Loading settings")
        try:
            with open("settings.json", "r", encoding="utf-8") as f:
                settings = json.load(f)
                crawler_settings = settings["crawler"]
                self.base_url = Constans.DEFAULT_URL
                self.price_min, self.price_max = self.__init_price(crawler_settings)
                self.province = self.__init_province(crawler_settings)
                self.city = self.__init_city(crawler_settings)
                self.district = self.__init_district(crawler_settings)
                self.property_type = self.__init_property_type(crawler_settings)
                self.auction_type = self.__init_auction_type(crawler_settings)
                self.mongo_db_host = self.__init_mongo_db_host(settings["database"])

        except Exception as e:
            logger.warning(
                f"Error loading the settings. Settings are set to default. Error: {e}",
            )
            self.set_default()
        logger.info("Running config: " + str(self.__dict__))

    @staticmethod
    def __init_price(settings: dict) -> (int, int):
        """
        Initialize the minimum and maximum price from the settings dictionary.

        If the price is not a dictionary or the minimum and maximum prices
        are not integers or are less than 0, a warning message is logged
        and the default prices are returned.

        :param settings: A dictionary containing the settings
        :return: A tuple containing the minimum and maximum price
        """
        price = settings.get("price")
        if not isinstance(price, dict):
            logger.warning("Prices is not of dict type. Price is set to default")
            return Constans.DEFAULT_PRICE_MIN, Constans.DEFAULT_PRICE_MAX

        price_min = price.get("min")
        price_max = price.get("max")

        if not isinstance(price_min, int):
            logger.warning("Min price is not of int type. Min price is set to default")
            price_min = Constans.DEFAULT_PRICE_MIN
        if not isinstance(price_max, int):
            logger.warning("Max price is not of int type. Max price is set to default")
            price_max = Constans.DEFAULT_PRICE_MAX
        if price_min < 0 or price_max < 0:
            logger.warning("Prices cannot be negative. Prices are set to default")
            return Constans.DEFAULT_PRICE_MIN, Constans.DEFAULT_PRICE_MAX
        if price_min > price_max:
            logger.warning(
                "Min price cannot be greater than max price. Prices are set to default"
            )
            return Constans.DEFAULT_PRICE_MIN, Constans.DEFAULT_PRICE_MAX

        return price_min, price_max

    @staticmethod
    def __init_province(settings: dict) -> str:
        """
        Initialize the province from the settings dictionary.

        If the province is not a string or is not in the list of available provinces,
        a warning message is logged and the default province is returned.

        :param settings: A dictionary containing the settings
        :return: The province
        """
        province = settings.get("province")
        if not isinstance(province, str):
            logger.warning("Province is not correct. Province is set to default")
            return Constans.DEFAULT_PROVINCE
        province = replace_polish_characters(province)
        if province not in AVAILABLE_PROVINCES:
            logger.warning("Province is not correct. Province is set to default")
            return Constans.DEFAULT_PROVINCE
        province = province.replace("-", "--")
        return province

    @staticmethod
    def __init_city(settings: dict) -> str:
        """
        Initialize the city from the settings dictionary.

        If the city is not a string,
        a warning message is logged and the default city is returned.

        :param settings: A dictionary containing the settings
        :return: The city
        """
        city = settings.get("city")
        if not isinstance(city, str):
            logger.warning("City is not correct. City is set to default")
            return Constans.DEFAULT_CITY
        return replace_polish_characters(city)

    @staticmethod
    def __init_district(settings: dict) -> str:
        """
        Initialize the district from the settings dictionary.

        If the district is not a string,
        a warning message is logged and the default district is returned.

        :param settings: A dictionary containing the settings
        :return: The district
        """
        district = settings.get("district")
        if not isinstance(district, str) or district == "":
            logger.warning("District is not correct. District is set to default")
            return Constans.DEFAULT_DISTRICT
        return replace_polish_characters(district)

    @staticmethod
    def __init_property_type(settings: dict) -> PropertyType:
        """
        Initialize the property type from the settings dictionary.

        If the property type is not a string or is not recognized,
        a warning message is logged and the default property type is returned.

        :param settings: A dictionary containing the settings
        :return: The property type
        """
        property_type_str = settings.get("property_type")
        if not isinstance(property_type_str, str):
            logger.warning(
                "Property type is not a string. Property type is set to default"
            )
            return Constans.DEFAULT_PROPERTY_TYPE

        property_type = get_property_type(property_type_str)
        if property_type is None:
            logger.warning(
                "Property type is not correct. Property type is set to default"
            )
            return Constans.DEFAULT_PROPERTY_TYPE

        return property_type

    @staticmethod
    def __init_auction_type(settings: dict) -> AuctionType:
        """
        Initialize the auction type from the settings dictionary.

        If the auction type is not a string or is not recognized,
        a warning message is logged and the default auction type is returned.

        :param settings: A dictionary containing the settings
        :return: The auction type
        """
        auction_type_str = settings.get("auction_type")
        if not isinstance(auction_type_str, str):
            logger.warning(
                "Auction type is not correct. Auction type is set to default"
            )
            return Constans.DEFAULT_AUCTION_TYPE

        auction_type = get_auction_type(auction_type_str)
        if auction_type is None:
            logger.warning(
                "Auction type is not correct. Auction type is set to default"
            )
            return Constans.DEFAULT_AUCTION_TYPE
        return auction_type

    def __init_mongo_db_host(self, settings: dict) -> str:
        """
        Initialize the mongo db host from the settings dictionary.

        If the mongo db host is not a string,
        a warning message is logged and the default mongo db host is returned.

        :param settings: A dictionary containing the settings
        :return: The mongo db host
        """
        mongo_db_host = settings.get("host")
        if not isinstance(mongo_db_host, str):
            logger.warning("Mongo db host is not correct")
            exit(1)
        return mongo_db_host

    def set_default(self):
        """
        Set the settings to their default values.

        These default values are defined in the Defaults class.
        """
        self.base_url = Constans.DEFAULT_URL
        self.price_min = Constans.DEFAULT_PRICE_MIN
        self.price_max = Constans.DEFAULT_PRICE_MAX
        self.province = Constans.DEFAULT_PROVINCE
        self.city = Constans.DEFAULT_CITY
        self.district = Constans.DEFAULT_DISTRICT
        self.property_type = Constans.DEFAULT_PROPERTY_TYPE
        self.auction_type = Constans.DEFAULT_AUCTION_TYPE
