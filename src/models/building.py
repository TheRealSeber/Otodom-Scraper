from mongoengine import EmbeddedDocument
from mongoengine import IntField
from mongoengine import StringField


class BuildingDocument(EmbeddedDocument):
    """
    Class representing a property building in the MongoDB database.
    """

    type = StringField()
    floors = IntField()
    build_year = IntField()

    def extract_data(self, properties: dict):
        """
        Extracts data about building from already converted JSON
        from the page to the dictionary.

        :param properties: The dict containing the building information
        """
        self.type = properties.get("Building_type", [None])[0]
        self.floors = properties.get("Building_floors_num", [None])[0]
        self.build_year = properties.get("Build_year")
