from src.clup.providers.basic_user_provider import BasicUserProvider
from src.clup.providers.basic_admin_provider import BasicAdminProvider
from src.clup.providers.basic_queue_provider import BasicQueueProvider
from src.clup.providers.basic_store_provider import BasicStoreProvider
from src.clup.providers.basic_reservation_provider \
    import BasicReservationProvider


bup = BasicUserProvider()
bap = BasicAdminProvider()

bsp = BasicStoreProvider()
bqp = BasicQueueProvider()
brp = BasicReservationProvider()
