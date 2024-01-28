import logging

from models import PropertyDocument
from mongoengine import QuerySet


class PropertyService:
    """
    Service responsible for interacting with the property documents in the database.
    """

    @classmethod
    def get_all(cls) -> list[PropertyDocument]:
        """
        :return: All the properties in the database
        """
        return PropertyDocument.objects.all()

    @classmethod
    def get_by_otodom_id(cls, otodom_id: int) -> PropertyDocument | None:
        """
        :param otodom_id: The otodom id of the property

        :return: The property document with the given otodom id
            or None if there is no property with the given otodom id
        """
        return PropertyDocument.objects(otodom_id=otodom_id).first()

    @classmethod
    def get_all_links(cls) -> set[PropertyDocument.link]:
        """
        :return: All the links of the properties in the database
        """
        properties: QuerySet = PropertyDocument.objects.all()
        return {property_.link for property_ in properties}

    @classmethod
    def put(cls, property_: PropertyDocument) -> PropertyDocument:
        """
        Inserts the property into the database.
        """
        try:
            property_.validate()
            property_ = property_.save()
            return property_
        except Exception as e:
            logging.warning(
                f"""Failed to insert property {property_.link} to database
            Error: {e}
            Property data: {property_.to_mongo().to_dict()}
            """
            )
