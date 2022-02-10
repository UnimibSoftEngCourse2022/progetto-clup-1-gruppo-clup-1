from sqlalchemy.orm import Session

from src.clup.database import User, Reservation, engine
from src.clup.entities import reservation


class SqliteReservationProvider:
    def get_user_reservation(self, user_id):
        db_session = Session(engine)
        query = db_session.query(Reservation).filter(Reservation.user_id == user_id)
        reservations = query.all()
        user_res = []
        for r in reservations:
            res = reservation.Reservation(id=r.id, user_id=r.user_id, aisle_id=r.aisle_id)
            user_res.append(res)
        return user_res


db_session = Session(engine)
user_from_db = db_session.query(User).filter(User.uuid == 1).all()[0]
rp = SqliteReservationProvider()
res = rp.get_user_reservation(user_from_db.uuid)
print(res)
