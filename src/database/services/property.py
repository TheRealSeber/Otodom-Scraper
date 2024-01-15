import logging

from database import PropertyDocument
from listing import Property
from mongoengine import QuerySet
from mongoengine.errors import NotUniqueError


class PropertyService:
    """
    Service responsible for interacting with the property documents in the database.
    """

    @classmethod
    def get_all_links(cls) -> set[str]:
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
        except NotUniqueError:
            pass
        except Exception as e:
            logging.warning(
                f"""Failed to insert property {property_.link} to database
            Error: {e}
            Property data: {property_.to_dict()}
            """
            )
