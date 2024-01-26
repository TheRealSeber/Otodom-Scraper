import json
import re

from bs4 import ResultSet


class Agency:
    """
    Represents an estate agency.
    """

    def __init__(self, code: ResultSet):
        """
        Initializes the estate agency instance.

        :param code: The HTML code containing the estate agency details
        """
        listing_information = json.loads(
            code.find("script", {"type": "application/json"}).text
        )
        agency_data = listing_information["props"]["pageProps"]["ad"]["agency"]
        self.name = agency_data["name"]
        self.otodom_id = agency_data["id"]
        (
            self.street,
            self.postal_code,
            self.city,
            self.county,
            self.province,
        ) = self.extract_estate_agency_address(agency_data)

    @staticmethod
    def extract_estate_agency_address(
        agency_data: dict,
    ) -> tuple[str, str, str, str, str]:
        """
        Extracts the details of the estate agency from the properties.

        There are three possible formats of the address:
        1. city, postal_code, street, county, province
        2. city, postal_code, street, province
        3. - , street, city, postal_code

        :param properties: The properties containing the estate agency details
        :return: The details of the estate agency
        """
        address_regex = r"^(.*?), (\d{2}-\d{3}), (.*), (.*), (.*)$"
        address = agency_data["address"]
        address_data = re.findall(address_regex, address)
        if not address_data:
            address_regex = r"^(.*?), (\d{2}-\d{3}), (.*), (.*)$"
            address_data = re.findall(address_regex, address)
            if not address_data:
                address_regex = r"^(.*), (.*?), (.*), (\d{2}-\d{3})$"
                address_data = re.findall(address_regex, address)
                if not address_data:
                    return address, None, None, None, None
                address_data = address_data[0]
                return (
                    address_data[1],
                    address_data[3],
                    address_data[2],
                    None,
                    None,
                )
            address_data = address_data[0]
            return (
                address_data[0],
                address_data[1],
                address_data[2],
                None,
                address_data[3],
            )
        address_data = address_data[0]
        return (
            address_data[0],
            address_data[1],
            address_data[2],
            address_data[3],
            address_data[4],
        )

    def to_dict(self):
        return {key: value for key, value in self.__dict__.items() if value is not None}
