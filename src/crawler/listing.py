from models import AgencyDocument
from models import PropertyDocument


class Listing:
    def __init__(self):
        self.property_: PropertyDocument = None
        self.agency: AgencyDocument | None = None

    @staticmethod
    def _flatten_listing(y: dict):
        """
        Flattens a JSON object to a single level.

        >>> flatten_json({"a": {"b": 1, "c": {"d": 2}})
            {"a_b": 1, "a_c_d": 2}
        """
        out = {}

        def flatten(x, name=""):
            if type(x) is dict:
                for a in x:
                    flatten(x[a], name + a + "_")
            elif type(x) is list:
                i = 0
                for a in x:
                    flatten(a, name + str(i) + "_")
                    i += 1
            else:
                out[name[:-1]] = x

        flatten(y)
        return out

    def to_dict(self):
        res = dict()
        property_ = self.property_.to_mongo().to_dict()
        res.update(property_)
        if self.agency is not None:
            agency = self.agency.to_mongo().to_dict()
            res["agency"] = agency
        return self._flatten_listing(res)
