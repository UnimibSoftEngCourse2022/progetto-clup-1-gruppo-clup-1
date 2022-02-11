from sqlalchemy.orm import Session

from src.clup.database import Reservation, engine
from src.clup.entities import reservation


class SqliteReservationProvider:
    def get_reservations(self):
        db_session = Session(engine)
        reservations = db_session.query(Reservation).all()
        reservations_ent = []
        for res_db in reservations:
            res_ent = reservation.Reservation(id=res_db.uuid, user_id=res_db.user_id, aisle_id=res_db.aisle_id)
            reservations_ent.append(res_ent)
        return reservations_ent

    def get_user_reservation(self, user_id):
        db_session = Session(engine)
        query = db_session.query(Reservation).filter(Reservation.user_id == user_id)
        reservations = query.all()
        user_res = []
        for r in reservations:
            res = reservation.Reservation(id=r.uuid, user_id=r.user_id, aisle_id=r.aisle_id)
            user_res.append(res)
        return user_res

    def get_reservations_with_id(self, reservation_id):
        db_session = Session(engine)
        reservations_same_id = db_session.query(Reservation).filter(Reservation.uuid == reservation_id).all()
        res_ents = []
        for res_w_id in reservations_same_id:
            res_ent = reservation.Reservation(id=res_w_id.uuid, aisle_id=res_w_id.aisle_id, user_id=res_w_id.user_id)
            res_ents.append(res_ent)
        return res_ents

    def add_reservation(self, reservation_ent):
        db_session = Session(engine)
        new_reservation = Reservation(uuid=reservation_ent.id, aisle_id=reservation_ent.aisle_id,
                                      user_id=reservation_ent.user_id)
        db_session.add(new_reservation)
        db_session.commit()

    def remove_reservation(self, reservation_id):
        db_session = Session(engine)
        db_session.query(Reservation).filter(Reservation.uuid == reservation_id).delete()
        db_session.commit()

    def remove_reservation_from_aisle(self, reservation_id, aisle_id):
        db_session = Session(engine)
        db_session.query(Reservation).filter((Reservation.uuid == reservation_id), (Reservation.aisle_id == aisle_id)) \
            .delete()
        db_session.commit()


rp = SqliteReservationProvider()
print(rp.get_reservations())
print(rp.get_user_reservation(1))
print(rp.get_reservations_with_id(2000))
rp.add_reservation(reservation.Reservation(id=2000, aisle_id=30, user_id=2))
print(rp.get_reservations_with_id(2000))
print(rp.get_reservations())
rp.remove_reservation_from_aisle(2000, 30)
print(rp.get_reservations())
