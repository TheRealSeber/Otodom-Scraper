from mongoengine import EmbeddedDocument
from mongoengine import FloatField
from mongoengine import StringField


class LocalizationDocument(EmbeddedDocument):

    """
    Class representing a property location in the MongoDB database.
    """

    province = StringField(required=True)
    city = StringField(required=True)
    district = StringField()
    street = StringField()
    county = StringField()
    latitude = FloatField()
    longitude = FloatField()

    def extract_data(self, properties: dict):
        """
        Extracts data about localization from already converted JSON
        from the page to the dictionary.

        :param properties: The dict containing the localization information
        """
        self.province = properties["address"]["province"]["code"]
        self.city = properties["address"]["city"]["code"]
        self.district = self.extract_district(properties["address"])
        self.street = self.extract_street(properties["address"])
        self.county = self.extract_county(properties["address"])
        self.latitude, self.longitude = self.extract_coordinates(properties)

    @staticmethod
    def extract_district(properties: dict) -> str:
        """
        Extracts the district from the properties.

        :param properties: The properties containing the district
        :return: The district
        """
        district = properties.get("district")
        if isinstance(district, dict):
            district = district["name"]
        return district

    @staticmethod
    def extract_street(properties: dict) -> str:
        """
        Extracts the street from the properties.

        :param properties: The properties containing the street
        :return: The street
        """
        street = properties.get("street")
        if isinstance(street, dict):
            street = street["name"]
            number = properties.get("number")
            if number is not None:
                street += " " + properties.get("number", "")
        return street

    @staticmethod
    def extract_county(properties: dict) -> str:
        """
        Extracts the county from the properties.

        :param properties: The properties containing the county
        :return: The county
        """
        county = properties.get("county")
        if isinstance(county, dict):
            county = county["code"]
        return county

    @staticmethod
    def extract_coordinates(properties: dict) -> tuple[float, float]:
        """
        Extracts the coordinates from the properties.

        :param properties: The properties containing the coordinates
        :return: The coordinates
        """
        coordinates = properties.get("coordinates")
        if coordinates is None:
            return None, None
        latitude = coordinates.get("latitude")
        longitude = coordinates.get("longitude")
        return latitude, longitude
