from src.clup.entities.exceptions import MaxCapacityReachedError


class SchedulerUseCase:
    def __init__(self, appointment_provider, reservation_provider, lane_provider):
        self.appointment_provider = appointment_provider
        self.reservation_provider = reservation_provider
        self.lane_provider = lane_provider

    def execute(self, date_time):
        appointments = self.appointment_provider.get_appointments()
        for appointment in appointments:
            if appointment.date_time == date_time and not self._already_pushed(appointment):
                reservations = self.reservation_provider.get_reservations_with_id(appointment.reservation_id)
                store_pool = self.lane_provider.get_store_pool(appointment.store_id)
                all_in_pools = True

                for reservation in reservations:
                    aisle_pool = self.lane_provider.get_aisle_pool(reservation.aisle_id)
                    try:
                        aisle_pool.add(reservation.id)
                    except MaxCapacityReachedError:
                        all_in_pools = False
                        waiting_queue = self.lane_provider.get_waiting_queue(reservation.aisle_id)
                        waiting_queue.push(reservation)

                if all_in_pools:
                    store_pool.add(reservation.id)

    def _already_pushed(self, appointment):
        reservations = self.reservation_provider.get_reservations_with_id(appointment.reservation_id)
        for reservation in reservations:
            try:
                aisle_pool = self.lane_provider.get_aisle_pool(reservation.aisle_id)
                waiting_queue = self.lane_provider.get_waiting_queue(reservation.aisle_id)
            except ValueError:
                return False
            if reservation.id in aisle_pool or waiting_queue:
                return True
        return False

