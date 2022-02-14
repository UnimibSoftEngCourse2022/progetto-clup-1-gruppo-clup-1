import uuid

from src.clup.entities.exceptions import MaxCapacityReachedError
from src.clup.entities.reservation import Reservation


class MakeReservationUseCase:
    def __init__(self, lane_provider, reservation_provider):
        self.lane_provider = lane_provider
        self.reservation_provider = reservation_provider

    def execute(self, user_id, store_id, aisle_ids):
        reservation_id = str(uuid.uuid1())

        for aisle_id in aisle_ids:
            reservation = Reservation(reservation_id, aisle_id, user_id)
            self.reservation_provider.add_reservation(reservation)

        all_in_pools = True
        for aisle_id in aisle_ids:
            aisle_pool = self.lane_provider.get_aisle_pool(aisle_id)
            store_pool = self.lane_provider.get_store_pool(store_id)
            try:
                aisle_pool.add(reservation_id)
            except MaxCapacityReachedError:
                all_in_pools = False
                waiting_queue = self.lane_provider.get_waiting_queue(aisle_id)
                waiting_queue.push(reservation.id)

        if all_in_pools:
            store_pool.add(reservation_id)

        return reservation_id
