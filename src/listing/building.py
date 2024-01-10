class Building:
    """
    Represents the building data of a given property.
    """

    def __init__(self, properties: dict):
        """
        Initializes the building instance.

        :param properties: Dictionary containing the information about the building
        """
        self.type: str | None = properties.get("Building_type", [None])[0]
        self.floors: str | None = properties.get("Building_floors_num", [None])[0]
        self.build_year: int | None = properties.get("Build_year")

    def to_dict(self):
        return {key: value for key, value in self.__dict__.items() if value is not None}
