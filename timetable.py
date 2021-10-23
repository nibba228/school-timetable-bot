from models import Lesson, Subject


class Timetable:
    def __init__(self, class_, group, weekday: int):
        self.class_ = class_
        self.class_group = class_ + str(group)
        self.weekday = weekday
     
    def get(self, session) -> list:
        timetable = session.query(
                Lesson.les_num,
                Subject.subj_name,
                Lesson.room,
                Lesson.time_start,
                Lesson.time_end
            ).join(Subject)\
            .filter(
            Lesson.class_.in_([self.class_, self.class_group]),
            Lesson.day_id == self.weekday).order_by(Lesson.les_num).all()
        
        
        return timetable