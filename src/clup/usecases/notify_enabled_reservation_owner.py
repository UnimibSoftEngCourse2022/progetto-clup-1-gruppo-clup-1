from src.clup.entities.observer_abc import Observer


class NotifyEnabledReservationOwner(Observer):
    def __init__(self, reservation_provider, user_provider, email_service_provider):
        self.reservation_provider = reservation_provider
        self.user_provider = user_provider
        self.email_service_provider = email_service_provider
        self.subject = 'Your reservation has been enabled'
        self.content = 'You can go shopping now!'

    def execute(self, reservation_id):
        try:
            user_id = self.reservation_provider.get_user_id(reservation_id)
            user = self.user_provider.get_user(user_id)
            self.email_service_provider.send(user.username, self.subject, self.content)
        except ValueError:
            pass

    def update(self, store_pool):
        reservation_id = store_pool.last_added
        self.execute(reservation_id)
