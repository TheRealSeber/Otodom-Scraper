import csv
import json
import logging

from common import Constans
from common import flatten_dict
from models import PropertyDocument
from mongoengine import QuerySet
from services import AgencyService


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

    @classmethod
    def to_csv_file(cls, filename: str, include_agencies: bool = False) -> None:
        """
        Saves the properties in the database to a csv file.

        :param filename: The name of the file
        """
        properties = cls.get_all()
        properties = [property_.to_mongo().to_dict() for property_ in properties]

        if include_agencies:
            agencies = AgencyService.get_all()
            agencies = [agency.to_mongo().to_dict() for agency in agencies]
            for property_ in properties:
                estate_agency = property_.get("estate_agency")
                if estate_agency is not None:
                    agency_id = str(estate_agency)
                    for agency in agencies:
                        if str(agency["_id"]) == agency_id:
                            property_["agency"] = agency
                            break

        with open(filename, "w", newline="", encoding="utf-8") as output_file:
            dict_writer = csv.DictWriter(output_file, Constans.CSV_KEYS)
            dict_writer.writeheader()
            dict_writer.writerows([flatten_dict(property_) for property_ in properties])

    @classmethod
    def to_json_file(cls, filename: str, include_agencies: bool = False) -> None:
        """
        Saves the properties in the database to a json file.

        :param filename: The name of the file
        """
        properties = cls.get_all()
        properties = [listing.to_mongo().to_dict() for listing in properties]

        if include_agencies:
            agencies = AgencyService.get_all()
            agencies = [agency.to_mongo().to_dict() for agency in agencies]
            for property_ in properties:
                estate_agency = property_.get("estate_agency")
                if estate_agency is not None:
                    agency_id = str(estate_agency)
                    for agency in agencies:
                        if str(agency["_id"]) == agency_id:
                            property_["agency"] = agency
                            break

        with open(filename, "w", encoding="utf-8") as file:
            json.dump(
                [flatten_dict(property_) for property_ in properties],
                file,
                ensure_ascii=False,
                default=str,
                indent=4,
            )
