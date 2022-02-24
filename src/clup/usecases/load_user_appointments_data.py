from collections import defaultdict


class LoadUserAppointmentsData:
    def __init__(self, store_provider, appointment_provider):
        self.store_provider = store_provider
        self.appointment_provider = appointment_provider

    def execute(self, user_id):
        appointments = \
            self.appointment_provider.get_user_appointments(user_id)

        stores = [self.store_provider.get_store(a.store_id) 
                  for a in appointments]

        data = []
        for appointment, store in zip(appointments, stores)
            data.append((appointment, store))
        return data
