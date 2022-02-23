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
        with Session(self.engine) as session, session.begin():
            query = session.query(models.Reservation). \
                filter(models.Reservation.user_id == user_id)
            model_reservations = query.all()
            reservations = [Reservation(mr.uuid, mr.aisle_id, mr.user_id)
                            for mr in model_reservations]
            return reservations
    
    def get_user_id(self, reservation_id):
        with Session(self.engine) as session, session.begin():
            query = session.query(models.Reservation). \
                filter(models.Reservation.uuid == reservation_id)
            model_reservations = query.all()
            user_ids = set(mr.user_id for mr in model_reservations)
            if len(user_ids) != 1:
                raise ValueError('something really wrong went here')
            return user_ids.pop()

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

    def get_store_from_reservation_id(self, reservation_id):
        with Session(self.engine) as session, session.begin():
            reservations = self.get_reservations_with_id(reservation_id)
            aisle_ids = [r.aisle_id for r in reservations]
            query = session.query(models.StoreAisle).all()
            store_id = [sa.store_uuid for sa in query if sa.aisle_uuid in aisle_ids]
            store_id = list(set(store_id))
            if len(store_id) != 1:
                raise ValueError("unable to find a store for this aisle")
            return store_id[0]

    def reservation_for_aisles_of_same_store(self, store_id, reservations_aisle_ids):
        with Session(self.engine) as session, session.begin():
            for aisle_id in reservations_aisle_ids:
                store_id_from_aisle = session.query(models.StoreAisle.store_uuid) \
                    .filter(models.StoreAisle.aisle_uuid == aisle_id).all()
                if store_id != store_id_from_aisle[0][0]:
                    raise ValueError("reservation for aisle in different stores")
