from loader import Session
from app.models.user import User
from loader import logger


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
        try:
            session = Session()
            user = User(
                from_id=from_id,
                class_=class_,
                group=group
            )
            session.add(user)
            session.commit()
            session.close()
        except:
            logger.exception(f'Ошибка при добавлении пользователя {from_id=}, {class_=}, {group=}')
        else:
            logger.info(f'Добавлен пользователь {from_id=}, {class_=}, {group=}')
    
    @staticmethod
    def delete(user: User):
        try:
            session = Session()
            session.delete(user)
            session.commit()
            session.close()
        except:
            logger.exception('Ошибка при удалении пользователя from_id={}, class_={}, group={}', user.from_id, user.class_, user.group)
        else:
            logger.info('Удален пользователь from_id={}, class_={}, group={}', user.from_id, user.class_, user.group)
