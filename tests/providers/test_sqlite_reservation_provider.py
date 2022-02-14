import unittest
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

import src.clup.database.models as models
from src.clup.entities.reservation import Reservation
from src.clup.providers.sqlite_reservation_provider \
    import SqliteReservationProvider


class TestSqliteReservationProvider(unittest.TestCase):
    def setUp(self):
        db_path = Path(__file__).parent
        self.db_file = db_path / Path('testdb.sqlite')
        self.engine = create_engine(f'sqlite:///{self.db_file}')
        models.Base.metadata.drop_all(self.engine)
        models.Base.metadata.create_all(self.engine)
        self.rp = SqliteReservationProvider(self.engine)

    def tearDown(self):
        self.db_file.unlink()

    def test_empty_sequence_returned_from_empty_db(self):
        reservations = self.rp.get_reservations()

        self.assertEqual(len(reservations), 0)

    def test_all_reservations_returned_from_non_empty_db(self):
        mr1 = models.Reservation(uuid='10', aisle_id='100', user_id='1000')
        mr2 = models.Reservation(uuid='20', aisle_id='200', user_id='2000')
        with Session(self.engine) as session, session.begin():
            session.add(mr1)
            session.add(mr2)

        reservations = self.rp.get_reservations()
        r1 = Reservation('10', '100', '1000')
        r2 = Reservation('20', '200', '2000')

        self.assertEqual(len(reservations), 2)
        self.assertTrue(r1 in reservations)
        self.assertTrue(r2 in reservations)

    def test_only_reservations_with_user_id_are_returned(self):
        mr1 = models.Reservation(uuid='10', aisle_id='100', user_id='1000')
        mr2 = models.Reservation(uuid='20', aisle_id='200', user_id='2000')
        with Session(self.engine) as session, session.begin():
            session.add(mr1)
            session.add(mr2)

        reservations = self.rp.get_user_reservations('1000')
        r = Reservation('10', '100', '1000')

        self.assertEqual(len(reservations), 1)
        self.assertTrue(r in reservations)

    def test_no_reservations_with_unexistent_user_id(self):
        mr1 = models.Reservation(uuid='10', aisle_id='100', user_id='1000')
        mr2 = models.Reservation(uuid='20', aisle_id='200', user_id='2000')
        with Session(self.engine) as session, session.begin():
            session.add(mr1)
            session.add(mr2)

        reservations = self.rp.get_user_reservations('9000')

        self.assertEqual(len(reservations), 0)

    def test_only_reservations_with_given_uuid_id_are_returned(self):
        mr1 = models.Reservation(uuid='10', aisle_id='100', user_id='1000')
        mr2 = models.Reservation(uuid='20', aisle_id='200', user_id='2000')
        mr3 = models.Reservation(uuid='20', aisle_id='300', user_id='2000')
        with Session(self.engine) as session, session.begin():
            session.add(mr1)
            session.add(mr2)
            session.add(mr3)

        reservations = self.rp.get_reservations_with_id('20')
        r1 = Reservation('20', '200', '2000')
        r2 = Reservation('20', '300', '2000')

        self.assertEqual(len(reservations), 2)
        self.assertTrue(r1 in reservations)
        self.assertTrue(r2 in reservations)

    def test_reservation_is_added_to_db(self):
        r = Reservation('10', '100', '1000')

        self.rp.add_reservation(r)

        with Session(self.engine) as session, session.begin():
            reservations = session.query(models.Reservation).all()
            reservation = reservations[0]

            self.assertEqual(len(reservations), 1)
            self.assertEqual(reservation.uuid, '10')
            self.assertEqual(reservation.aisle_id, '100')
            self.assertEqual(reservation.user_id, '1000')

    def test_reservation_is_removed_from_db(self):
        mr1 = models.Reservation(uuid='10', aisle_id='100', user_id='1000')
        with Session(self.engine) as session, session.begin():
            session.add(mr1)

        self.rp.delete_reservation('10')

        with Session(self.engine) as session, session.begin():
            reservations = session.query(models.Reservation).all()

            self.assertEqual(len(reservations), 0)

    def test_reservation_with_given_aisle_is_removed(self):
        mr2 = models.Reservation(uuid='20', aisle_id='200', user_id='2000')
        mr3 = models.Reservation(uuid='20', aisle_id='300', user_id='2000')
        with Session(self.engine) as session, session.begin():
            session.add(mr2)
            session.add(mr3)

        reservations = self.rp.delete_reservation_from_aisle('20', '200')

        with Session(self.engine) as session, session.begin():
            reservations = session.query(models.Reservation).all()
            reservation = reservations[0]

            self.assertEqual(len(reservations), 1)
            self.assertEqual(reservation.uuid, '20')
            self.assertEqual(reservation.aisle_id, '300')
            self.assertEqual(reservation.user_id, '2000')
