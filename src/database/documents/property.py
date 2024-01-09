from common import AuctionType
from common import ConstructionStatus
from common import MarketType
from common import OfferedBy
from common import PropertyType
from mongoengine import BooleanField
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
    type = StringField()
    floors = IntField()
    build_year = IntField()


class Location(EmbeddedDocument):
    province = StringField(required=True)
    city = StringField(required=True)
    district = StringField(required=True)
    street = StringField()
    county = StringField()


class PropertyDocument(Document):
    link = URLField(required=True)
    promoted = BooleanField(required=True, default=False)
    otodom_id = IntField(required=True, unique=True)
    title = StringField(required=True)
    area = FloatField(required=True)
    floor = StringField()
    price = IntField()
    price_per_meter = IntField()
    rooms = IntField()
    heating = StringField()
    rent = IntField()
    property_type = EnumField(PropertyType, required=True)
    market_type = EnumField(MarketType, required=True)
    auction_type = EnumField(AuctionType, required=True)
    localization = EmbeddedDocumentField(Location, required=True)
    construction_status = EnumField(ConstructionStatus)
    building = EmbeddedDocumentField(Building)
    offered_by = EnumField(OfferedBy, required=True)
    estate_agency = ReferenceField("Agencies")

    meta = {"collection": "Properties"}
