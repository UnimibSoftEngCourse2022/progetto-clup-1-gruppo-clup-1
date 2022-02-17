class CancelAppointmentUseCase:
    def __init__(self, appointment_provider, reservation_provider):
        self.appointment_provider = appointment_provider
        self.reservation_provider = reservation_provider

    def execute(self, user_id, reservation_id):
        try:
            self.appointment_provider.delete_appointment(reservation_id)
        except ValueError:
            raise

        try:
            self.reservation_provider.remove_reservation_with_user_check(reservation_id, user_id)
        except ValueError:
            raise
