import logging

from database import AgencyDocument
from listing import Agency
from mongoengine.errors import NotUniqueError


class AgencyService:
    """
    Service responsible for interacting with the agency documents in the database.
    """

    @classmethod
    def get_by_otodom_id(cls, otodom_id: int) -> AgencyDocument | None:
        """
        :param otodom_id: The otodom id of the agency

        :return: The agency document with the given otodom id
            or None if there is no agency with the given otodom id
        """
        return AgencyDocument.objects(otodom_id=otodom_id).first()

    @classmethod
    def put(cls, agency: Agency) -> None:
        try:
            agency_doc = AgencyDocument(**agency.to_dict())
            agency_doc.save()
        except NotUniqueError:
            pass
        except Exception as e:
            logging.warning(
                f"""Failed to insert agency {agency.name} to database
            Error: {e}
            Agency data: {agency.to_dict()}
            """
            )
