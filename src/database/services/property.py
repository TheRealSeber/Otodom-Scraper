from database import PropertyDocument
from listing import Property
from mongoengine import QuerySet


class PropertyService:
    """
    Service responsible for interacting with the property documents in the database.
    """

    @classmethod
    def get_all_links(cls) -> set:
        """
        :return: All the links of the properties in the database
        """
        properties: QuerySet = PropertyDocument.objects.all()
        return {property_.link for property_ in properties}

    @classmethod
    def put(cls, property_: Property) -> None:
        """
        Inserts the property into the database.
        """
        try:
            property_doc = PropertyDocument(**property_.to_dict())
            property_doc.save()
        except Exception as e:
            print(e)
            print(property_.to_dict())
