from loader import Session
from app.models.user import User


class Users:

    @staticmethod
    def get(from_id: int) -> bool:
        session = Session()
        user = session.query(User).get(from_id)
        if user:
            session.expunge(user)
        session.close()

        return user
    
    @staticmethod
    def insert(from_id: int, class_: str, group: int) -> None:
        session = Session()
        user = User(
            from_id=from_id,
            class_=class_,
            group=group
        )
        session.add(user)
        session.commit()
        session.close()
    
    @staticmethod
    def delete(user: User):
        session = Session()
        session.delete(user)
        session.commit()
        session.close()
