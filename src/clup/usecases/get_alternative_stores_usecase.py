from src.clup.usecases.filter_aisle_by_categories_usecase import FilterAisleByCategoriesUseCase
from src.clup.usecases.make_appointment_usecase import MakeAppointmentUseCase


class GetAlternativeStoresUseCase:
    def __init__(self, store_provider, aisle_provider, reservation_provider, appointment_provider):
        self.store_provider = store_provider
        self.aisle_provider = aisle_provider
        self.reservation_provider = reservation_provider
        self.appointment_provider = appointment_provider

    def execute(self, categories, date):
        valid_stores = []
        stores = self.store_provider.get_stores()
        fabc = FilterAisleByCategoriesUseCase(self.aisle_provider)
        for store in stores:
            try:
                aisle_ids = fabc.execute(store.id, categories)
                mauc = MakeAppointmentUseCase(
                    reservation_provider=self.reservation_provider,
                    appointment_provider=self.appointment_provider,
                    aisle_provider=self.aisle_provider,)
                if mauc.check_enough_spaces_in_aisles(aisle_ids, date):
                    valid_stores.append(store)

            except ValueError:
                continue
        return valid_stores
