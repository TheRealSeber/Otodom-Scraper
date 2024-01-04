import json
import logging

from settings.s_types import AuctionType
from settings.s_types import Defaults
from settings.s_types import PropertyType
from settings.utils import get_auction_type
from settings.utils import get_property_type
from settings.utils import replace_polish_characters

AVAILABLE_PROVINCES = [
    "dolnoslaskie",
    "kujawsko-pomorskie",
    "lubelskie",
    "lubuskie",
    "lodzkie",
    "malopolskie",
    "mazowieckie",
    "opolskie",
    "podkarpackie",
    "podlaskie",
    "pomorskie",
    "slaskie",
    "swietokrzyskie",
    "warminsko-mazurskie",
    "wielkopolskie",
    "zachodniopomorskie",
]


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
        logging.info("Loading settings")
        try:
            with open("settings.json", "r", encoding="utf-8") as f:
                settings = json.load(f)
                self.base_url = Defaults.DEFAULT_URL
                self.price_min, self.price_max = self.__init_price(settings)
                self.province = self.__init_province(settings)
                self.city = self.__init_city(settings)
                self.district = self.__init_district(settings)
                self.property_type = self.__init_property_type(settings)
                self.auction_type = self.__init_auction_type(settings)

        except Exception as e:
            logging.warning(
                "Settings file not found. Settings are set to default. Error info: %s",
                e,
            )
            self.set_default()

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
        logging.info(price)
        if not isinstance(price, dict):
            logging.warning("Prices is not of dict type. Price is set to default")
            return Defaults.DEFAULT_PRICE_MIN, Defaults.DEFAULT_PRICE_MAX

        price_min = price.get("min")
        price_max = price.get("max")

        if not isinstance(price_min, int):
            logging.warning("Min price is not of int type. Min price is set to default")
            price_min = Defaults.DEFAULT_PRICE_MIN
        if not isinstance(price_max, int):
            logging.warning("Max price is not of int type. Max price is set to default")
            price_max = Defaults.DEFAULT_PRICE_MAX
        if price_min < 0 or price_max < 0:
            logging.warning("Prices cannot be negative. Prices are set to default")
            return Defaults.DEFAULT_PRICE_MIN, Defaults.DEFAULT_PRICE_MAX
        if price_min > price_max:
            logging.warning(
                "Min price cannot be greater than max price. Prices are set to default"
            )
            return Defaults.DEFAULT_PRICE_MIN, Defaults.DEFAULT_PRICE_MAX

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
            logging.warning("Province is not correct. Province is set to default")
            return Defaults.DEFAULT_PROVINCE
        province = replace_polish_characters(province)
        if province not in AVAILABLE_PROVINCES:
            logging.warning("Province is not correct. Province is set to default")
            return Defaults.DEFAULT_PROVINCE
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
            logging.warning("City is not correct. City is set to default")
            return Defaults.DEFAULT_CITY
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
            logging.warning("District is not correct. District is set to default")
            return Defaults.DEFAULT_DISTRICT
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
            logging.warning(
                "Property type is not a string. Property type is set to default"
            )
            return Defaults.DEFAULT_PROPERTY_TYPE

        property_type = get_property_type(property_type_str)
        if property_type is None:
            logging.warning(
                "Property type is not correct. Property type is set to default"
            )
            return Defaults.DEFAULT_PROPERTY_TYPE

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
            logging.warning(
                "Auction type is not correct. Auction type is set to default"
            )
            return Defaults.DEFAULT_AUCTION_TYPE

        auction_type = get_auction_type(auction_type_str)
        if auction_type is None:
            logging.warning(
                "Auction type is not correct. Auction type is set to default"
            )
            return Defaults.DEFAULT_AUCTION_TYPE
        return auction_type

    def set_default(self):
        """
        Set the settings to their default values.

        These default values are defined in the Defaults class.
        """
        self.base_url = Defaults.DEFAULT_URL
        self.price_min = Defaults.DEFAULT_PRICE_MIN
        self.price_max = Defaults.DEFAULT_PRICE_MAX
        self.province = Defaults.DEFAULT_PROVINCE
        self.city = Defaults.DEFAULT_CITY
        self.district = Defaults.DEFAULT_DISTRICT
        self.property_type = Defaults.DEFAULT_PROPERTY_TYPE
        self.auction_type = Defaults.DEFAULT_AUCTION_TYPE
