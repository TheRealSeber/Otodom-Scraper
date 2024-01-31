import json
import re

from bs4 import ResultSet
from mongoengine import Document
from mongoengine import IntField
from mongoengine import StringField


class AgencyDocument(Document):
    """
    Class representing an agency document in the MongoDB database.
    """

    name = StringField(required=True)
    otodom_id = IntField(required=True, unique=True)
    street = StringField(required=True)
    city = StringField()
    province = StringField()
    postal_code = StringField()
    county = StringField()

    meta = {"collection": "Agencies"}

    def extract_data(self, code: ResultSet):
        """
        Extracts data from the page and updates the property instance.

        This method loads the property information from a script tag in the HTML code,
        parses it as JSON and uses it to update the attributes of the property instance.

        :param code: The HTML code containing the property information
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
        3. _ , street, city, postal_code

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
