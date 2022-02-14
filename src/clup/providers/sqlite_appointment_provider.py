from sqlalchemy.orm import Session

import src.clup.database.models as models
from src.clup.entities.appointment import Appointment


class SqliteAppointmentProvider:
    def __init__(self, engine):
        self.engine = engine

    def add_appointment(self, reservation_id, date):
        with Session(self.engine) as session, session.begin():
            model_appointment = models.Appointment(
                reservation_uuid=reservation_id,
                date=date
            )
            session.add(model_appointment)

    def get_appointments(self):
        with Session(self.engine) as session, session.begin():
            query = session.query(models.Appointment)
            appointments_model = query.all()
            appointments = []
            for app_m in appointments_model:
                appointment = Appointment(
                    reservation_id=app_m.reservation_uuid,
                    store_id=app_m.store_id,
                    date_time=app_m.date_time
                )
                appointments.append(appointment)
            return appointments

    def get_appointment(self, reservation_id):
        with Session(self.engine) as session, session.begin():
            query = session.query(models.Appointment). \
                filter(models.Appointment.reservation_uuid == reservation_id)
            reservation = query.all()[0]
            return reservation

    def delete_appointment(self, reservation_id):
        with Session(self.engine) as session, session.begin():
            if reservation_id not in [ap.reservation_id for ap in self.get_appointments()]:
                raise ValueError("Reservation id not existing")
            query = session.query(models.Appointment)\
                .filter(models.Appointment.reservation_uuid == reservation_id).delete()