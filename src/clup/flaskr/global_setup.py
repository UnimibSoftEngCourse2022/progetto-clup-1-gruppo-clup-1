from src.clup.database import engine
from src.clup.providers.basic_lane_provider import BasicLaneProvider
from src.clup.providers.sqlite_admin_provider import SqliteAdminProvider
from src.clup.providers.sqlite_aisle_provider import SqliteAisleProvider
from src.clup.providers.sqlite_appointment_provider \
    import SqliteAppointmentProvider
from src.clup.providers.sqlite_reservation_provider \
    import SqliteReservationProvider
from src.clup.providers.sqlite_store_manager_provider \
    import SqliteStoreManagerProvider
from src.clup.providers.sqlite_store_provider import SqliteStoreProvider
from src.clup.providers.sqlite_user_provider import SqliteUserProvider
from src.clup.providers.gmail_service_provider import GmailServiceProvider

from src.clup.usecases.notify_enabled_reservation_owner \
    import NotifyEnabledReservationOwner
from src.clup.usecases.init_lanes import InitLanes


user_provider = SqliteUserProvider(engine)
admin_provider = SqliteAdminProvider(engine)
store_manager_provider = SqliteStoreManagerProvider(engine)

store_provider = SqliteStoreProvider(engine)
aisle_provider = SqliteAisleProvider(engine)
lane_provider = BasicLaneProvider()

reservation_provider = SqliteReservationProvider(engine)
appointment_provider = SqliteAppointmentProvider(engine)

email_service_provider = GmailServiceProvider('clup.se.project@gmail.com', 'Sonar4Life!')

notifier = NotifyEnabledReservationOwner(reservation_provider,
                                         user_provider,
                                         email_service_provider)

il = InitLanes(lane_provider, aisle_provider, store_provider, notifier)
il.execute()
