class Localization:
    """
    Represents the localization of a listing.

    :param properties: The properties dictionary containing the localization
    """

    def __init__(self, properties: dict):
        self.province = properties["province"]["code"]
        self.city = properties["city"]["code"]
        self.district = self.extract_district(properties)
        self.street = self.extract_street(properties)
        self.county = self.extract_county(properties)

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

    def to_dict(self):
        return {key: value for key, value in self.__dict__.items() if value is not None}
