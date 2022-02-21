from src.clup.database import engine
from src.clup.providers.basic_lane_provider import BasicLaneProvider
from src.clup.providers.sqlite_aisle_provider import SqliteAisleProvider
from src.clup.providers.sqlite_appointment_provider \
    import SqliteAppointmentProvider
from src.clup.providers.sqlite_store_manager_provider \
    import SqliteStoreManagerProvider
from src.clup.providers.sqlite_reservation_provider \
    import SqliteReservationProvider
from src.clup.providers.sqlite_store_provider import SqliteStoreProvider
from src.clup.providers.sqlite_user_provider import SqliteUserProvider
from src.clup.providers.sqlite_admin_provider import SqliteAdminProvider


user_provider = SqliteUserProvider(engine)
admin_provider = SqliteAdminProvider(engine)
store_manager_provider = SqliteStoreManagerProvider(engine)

store_provider = SqliteStoreProvider(engine)
aisle_provider = SqliteAisleProvider(engine)
lane_provider = BasicLaneProvider()
reservation_provider = SqliteReservationProvider(engine)
appointment_provider = SqliteAppointmentProvider(engine)
