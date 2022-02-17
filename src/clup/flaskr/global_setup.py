from src.clup.database import engine
from src.clup.providers.basic_admin_provider import BasicAdminProvider
from src.clup.providers.basic_lane_provider import BasicLaneProvider
from src.clup.providers.basic_user_provider import BasicUserProvider
from src.clup.providers.sqlite_aisle_provider import SqliteAisleProvider
from src.clup.providers.sqlite_appointment_provider import SqliteAppointmentProvider
from src.clup.providers.sqlite_reservation_provider import SqliteReservationProvider
from src.clup.providers.sqlite_store_provider import SqliteStoreProvider

user_provider = BasicUserProvider()
admin_provider = BasicAdminProvider()

store_provider = SqliteStoreProvider(engine)
aisle_provider = SqliteAisleProvider(engine)
lane_provider = BasicLaneProvider()
reservation_provider = SqliteReservationProvider(engine)
appointment_provider = SqliteAppointmentProvider(engine)
