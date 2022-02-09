from src.clup.providers.basic_admin_provider import BasicAdminProvider
from src.clup.providers.basic_lane_provider import BasicLaneProvider
from src.clup.providers.basic_reservation_provider \
    import BasicReservationProvider
from src.clup.providers.basic_store_provider import BasicStoreProvider
from src.clup.providers.basic_user_provider import BasicUserProvider

bup = BasicUserProvider()
bap = BasicAdminProvider()

bsp = BasicStoreProvider()
bqp = BasicLaneProvider()
brp = BasicReservationProvider()
