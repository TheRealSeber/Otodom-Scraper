from database import AgencyDocument
from listing import Agency


class AgencyService:
    @classmethod
    def get_by_otodom_id(cls, otodom_id: int) -> AgencyDocument:
        return AgencyDocument.objects(otodom_id=otodom_id).first()

    @classmethod
    def put(cls, agency: Agency) -> None:
        try:
            agency_doc = AgencyDocument(**agency.to_dict())
            agency_doc.save()
        except Exception as e:
            print(e)
            print(agency.to_dict())
