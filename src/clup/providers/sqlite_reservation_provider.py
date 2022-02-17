from sqlalchemy.orm import Session

import src.clup.database.models as models
from src.clup.entities.reservation import Reservation
from src.clup.providers.reservation_provider_abc \
    import ReservationProvider


class SqliteReservationProvider(ReservationProvider):
    def __init__(self, engine):
        self.engine = engine

    def get_reservations(self):
        with Session(self.engine) as session, session.begin():
            model_reservations = session.query(models.Reservation).all()
            reservations = [Reservation(mr.uuid, mr.aisle_id, mr.user_id)
                            for mr in model_reservations]
            return reservations

    def get_user_reservations(self, user_id):
        if user_id not in [res.user_id for res in self.get_reservations()]:
            raise ValueError('user_id not present, unable to find his reservations')

        with Session(self.engine) as session, session.begin():
            query = session.query(models.Reservation). \
                filter(models.Reservation.user_id == user_id)
            model_reservations = query.all()
            reservations = [Reservation(mr.uuid, mr.aisle_id, mr.user_id)
                            for mr in model_reservations]
            return reservations

    def get_reservations_with_id(self, reservation_id):
        with Session(self.engine) as session, session.begin():
            query = session.query(models.Reservation). \
                filter(models.Reservation.uuid == reservation_id)
            model_reservations = query.all()

            if len(model_reservations) == 0:
                raise ValueError("reservation_id not valid, unable to find any reservation")

            reservations = [Reservation(mr.uuid, mr.aisle_id, mr.user_id)
                            for mr in model_reservations]
            return reservations

    def add_reservation(self, reservation):
        with Session(self.engine) as session, session.begin():
            model_reservation = models.Reservation(
                uuid=reservation.id,
                aisle_id=reservation.aisle_id,
                user_id=reservation.user_id,
            )
            session.add(model_reservation)

    def update_reservation(self, reservation):
        raise NotImplementedError()

    def delete_reservation(self, reservation_id):
        if reservation_id not in [r.id for r in self.get_reservations()]:
            raise ValueError("unable to delete reservation, not existing")
        with Session(self.engine) as session, session.begin():
            query = session.query(models.Reservation). \
                filter(models.Reservation.uuid == reservation_id)
            query.delete()

    def remove_reservation_with_user_check(self, reservation_id, user_id):
        if reservation_id not in [r.id for r in self.get_reservations()]:
            raise ValueError("unable to delete reservation, not existing")
        with Session(self.engine) as session, session.begin():
            query = session.query(models.Reservation). \
                filter(models.Reservation.uuid == reservation_id,
                       models.Reservation.user_id == user_id)
            query.delete()

    def delete_reservation_from_aisle(self, reservation_id, aisle_id):
        with Session(self.engine) as session, session.begin():
            query = session.query(models.Reservation). \
                filter(models.Reservation.uuid == reservation_id). \
                filter(models.Reservation.aisle_id == aisle_id)
            query.delete()
