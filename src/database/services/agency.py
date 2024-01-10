from database import AgencyDocument
from listing import Agency


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
        except Exception as e:
            print(e)
            print(agency.to_dict())
