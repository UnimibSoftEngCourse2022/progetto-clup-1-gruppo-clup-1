from src.clup.providers.basic_admin_provider import BasicAdminProvider
from src.clup.providers.basic_aisle_provider import BasicAisleProvider
from src.clup.providers.basic_lane_provider import BasicLaneProvider
from src.clup.providers.basic_reservation_provider \
    import BasicReservationProvider
from src.clup.providers.basic_store_provider import BasicStoreProvider
from src.clup.providers.basic_user_provider import BasicUserProvider

user_provider = BasicUserProvider()
admin_provider = BasicAdminProvider()

store_provider = BasicStoreProvider()
aisle_provider = BasicAisleProvider()
lane_provider = BasicLaneProvider()
reservation_provider = BasicReservationProvider()
