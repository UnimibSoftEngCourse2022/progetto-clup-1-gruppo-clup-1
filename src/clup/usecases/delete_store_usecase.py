from src.clup.entities.store import Store

class DeleteStoreUseCase:
    def __init__(self, store_provider):
        self.store_provider = store_provider

    def execute(self, store_id):
        stores = self.store_provider.get_stores()
        found = False
        for store_item in stores:
            if store_item.id == store_id:
                self.store_provider.delete_store(store_id)
                found = True

        if not found:
            raise ValueError('store isnt in the stores list')
            
        return stores