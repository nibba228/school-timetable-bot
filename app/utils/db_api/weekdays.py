from app.models.school import Week
from loader import Session


class WeekDays:

    @staticmethod
    def get_day_name(weekday: int) -> str:
        session = Session()
        day_name = session.query(Week).get(weekday).day_name
        session.close()

        return day_name
