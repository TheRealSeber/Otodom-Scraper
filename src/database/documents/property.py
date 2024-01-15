from common import AuctionType
from common import ConstructionStatus
from common import MarketType
from common import OfferedBy
from common import PropertyType
from mongoengine import BooleanField
from mongoengine import DateTimeField
from mongoengine import Document
from mongoengine import EmbeddedDocument
from mongoengine import EmbeddedDocumentField
from mongoengine import EnumField
from mongoengine import FloatField
from mongoengine import IntField
from mongoengine import ReferenceField
from mongoengine import StringField
from mongoengine import URLField


class Building(EmbeddedDocument):
    """
    Class representing a property building in the MongoDB database.
    """

    type = StringField()
    floors = IntField()
    build_year = IntField()


class Localization(EmbeddedDocument):

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


class PropertyDocument(Document):
    """
    Class representing a property document in the MongoDB database.
    """

    link = URLField(required=True)
    promoted = BooleanField(required=True, default=False)
    otodom_id = IntField(required=True, unique=True)
    created_at = DateTimeField(required=True)
    title = StringField(required=True)
    area = FloatField(required=True)
    floor = StringField()
    price = IntField()
    price_per_meter = IntField()
    rooms = StringField()
    heating = StringField()
    extras = StringField()
    security_types = StringField()
    rent = IntField()
    property_type = EnumField(PropertyType, required=True)
    market_type = EnumField(MarketType, required=True)
    auction_type = EnumField(AuctionType, required=True)
    localization = EmbeddedDocumentField(Localization, required=True)
    construction_status = EnumField(ConstructionStatus)
    building = EmbeddedDocumentField(Building)
    offered_by = EnumField(OfferedBy, required=True)
    estate_agency = ReferenceField("Agencies")

    meta = {"collection": "Properties"}
