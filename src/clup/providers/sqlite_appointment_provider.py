from sqlalchemy.orm import Session

import src.clup.database.models as models


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

    def get_appointments_id(self):
        with Session(self.engine) as session, session.begin():
            query = session.query(models.Appointment.reservation_uuid)
            appointments_id = query.all()
            return [str(app_id) for app_id in appointments_id]

    def get_appointment(self, reservation_id):
        with Session(self.engine) as session, session.begin():
            query = session.query(models.Appointment).\
                filter(models.Appointment.reservation_uuid == reservation_id)
            reservation = query.all()[0]
            return reservation