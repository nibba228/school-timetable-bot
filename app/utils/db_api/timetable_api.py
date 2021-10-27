from app.models.school import Lesson, Subject
from loader import Session


class Timetable:

    @staticmethod
    def get(class_: str, group: int, weekday: int) -> list:
        class_group = class_ + str(group)
        session = Session()
        timetable = session.query(
                Lesson.les_num,
                Subject.subj_name,
                Lesson.room,
                Lesson.time_start,
                Lesson.time_end
            ).join(Subject)\
            .filter(
                Lesson.class_.in_([class_, class_group]),
                Lesson.day_id == weekday
            ).order_by(Lesson.les_num).all()
        
        session.close()    
        return timetable