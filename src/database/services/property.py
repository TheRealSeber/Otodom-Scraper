from database import PropertyDocument
from listing import Property
from mongoengine import QuerySet


class PropertyService:
    @classmethod
    def get_all_links(cls) -> set:
        properties: QuerySet = PropertyDocument.objects.all()
        return {property_.link for property_ in properties}

    @classmethod
    def put(cls, property_: Property) -> None:
        try:
            property_doc = PropertyDocument(**property_.to_dict())
            property_doc.save()
        except Exception as e:
            print(e)
            print(property_.to_dict())
