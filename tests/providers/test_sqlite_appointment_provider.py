import datetime
import unittest
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

import src.clup.database.models as models
from src.clup.entities.appointment import Appointment
from src.clup.providers.sqlite.sqlite_appointment_provider \
    import SqliteAppointmentProvider


class TestSqliteAppointmentProvider(unittest.TestCase):
    def setUp(self):
        db_path = Path(__file__).parent
        self.db_file = db_path / Path('appointmentprovider_testdb.sqlite')
        self.engine = create_engine(f'sqlite:///{self.db_file}')
        models.Base.metadata.drop_all(self.engine)
        models.Base.metadata.create_all(self.engine)
        self.ap = SqliteAppointmentProvider(self.engine)

    def tearDown(self):
        self.db_file.unlink()

    def test_empty_sequence_returned_from_empty_db(self):
        appointments = self.ap.get_appointments()

        self.assertEqual(len(appointments), 0)

    def test_all_appointments_returned_from_non_empty_db(self):
        dt = datetime.datetime.now()
        ma1 = models.Appointment(reservation_uuid='10', store_id='s1', date_time=dt)
        ma2 = models.Appointment(reservation_uuid='20', store_id='s2', date_time=dt)
        with Session(self.engine) as session, session.begin():
            session.add(ma1)
            session.add(ma2)

        appointments = self.ap.get_appointments()
        a1 = Appointment('10', 's1', dt)
        a2 = Appointment('20', 's2', dt)

        self.assertEqual(len(appointments), 2)
        self.assertTrue(a1 in appointments)
        self.assertTrue(a2 in appointments)

    def test_appointment_is_added_to_db(self):
        dt = datetime.datetime.now()
        a = Appointment('10', 's1', dt)

        self.ap.add_appointment(a)

        with Session(self.engine) as session, session.begin():
            appointments = session.query(models.Appointment).all()
            appointment = appointments[0]

            self.assertEqual(len(appointments), 1)
            self.assertEqual(appointment.reservation_uuid, '10')
            self.assertEqual(appointment.store_id, 's1')
            self.assertEqual(appointment.date_time, dt)

    def test_appointment_is_removed_from_db(self):
        dt = datetime.datetime.now()
        ma1 = models.Appointment(reservation_uuid='10', store_id='u1', date_time=dt)
        with Session(self.engine) as session, session.begin():
            session.add(ma1)

        self.ap.delete_appointment('10')

        with Session(self.engine) as session, session.begin():
            appointments = session.query(models.Appointment).all()

            self.assertEqual(len(appointments), 0)

    def test_only_user_appointments_are_returned(self):
        dt = datetime.datetime.now()
        mr1 = models.Reservation(uuid='10', aisle_id='aisle_id', user_id='user_id')
        mr2 = models.Reservation(uuid='20', aisle_id='aisle_id', user_id='other_id')
        ma1 = models.Appointment(reservation_uuid='10', store_id='s1', date_time=dt)
        ma2 = models.Appointment(reservation_uuid='20', store_id='s1', date_time=dt)
        with Session(self.engine) as session, session.begin():
            session.add(ma1)
            session.add(ma2)
            session.add(mr1)
            session.add(mr2)

        appointments = self.ap.get_user_appointments('user_id')
        a = Appointment('10', 's1', dt)

        self.assertEqual(len(appointments), 1)
        self.assertTrue(a in appointments)
