from common import flatten_dict
from models import AgencyDocument
from models import PropertyDocument


class Listing:
    def __init__(self):
        self.property_: PropertyDocument = None
        self.agency: AgencyDocument | None = None

    def to_dict(self) -> dict:
        """
        Converts the listing to a python dictionary instance.

        :return: The listing as a python dictionary instance
        """
        res = dict()
        property_ = self.property_.to_mongo().to_dict()
        res.update(property_)
        if self.agency is not None:
            agency = self.agency.to_mongo().to_dict()
            res["agency"] = agency
        return flatten_dict(res)
