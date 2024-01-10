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
