from sqlalchemy import Column, Integer, String, Time
from sqlalchemy.schema import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    from_id = Column(Integer, primary_key=True, unique=True)
    class_ = Column(String(3), nullable=False)
    group = Column(Integer, nullable=False)


class Week(Base):
    __tablename__ = 'week'
    day_id = Column(Integer, primary_key=True)
    day_name = Column(String(20), nullable=False)
    lessons = relationship('Lesson', backref='day_lessons')


class Subject(Base):
    __tablename__ = 'subject'
    subj_id = Column(Integer, primary_key=True)
    subj_name = Column(String(30), nullable=False)
    lessons = relationship('Lesson', backref='subj_lessons')


class Lesson(Base):
    __tablename__ = 'lesson'
    id = Column(Integer, primary_key=True)
    class_ = Column(String(5), nullable=False)
    day_id = Column(Integer, ForeignKey('week.day_id'), nullable=False)
    les_num = Column(Integer, nullable=False)
    subj_id = Column(Integer, ForeignKey('subject.subj_id'), nullable=False)
    room = Column(String(15), nullable=False)
    time_start = Column(String(5), nullable=False)
    time_end = Column(String(5), nullable=False)