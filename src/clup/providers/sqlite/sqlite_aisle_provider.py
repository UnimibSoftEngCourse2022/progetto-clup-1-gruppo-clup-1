from sqlalchemy.orm import Session

import src.clup.database.models as models
from src.clup.entities.aisle import Aisle
from src.clup.entities.category import Category
from src.clup.providers.abc.aisle_provider \
    import AisleProvider


class SqliteAisleProvider(AisleProvider):
    def __init__(self, engine):
        self.engine = engine

    def _get_categories(self, categories_str):
        category_ints = [int(c) for c in categories_str.split(',')]
        categories = [Category(i) for i in sorted(category_ints)]
        return tuple(categories)

    def get_aisles(self):
        with Session(self.engine) as session, session.begin():
            query = session.query(models.Aisle)
            model_aisles = query.all()
            aisles = [Aisle(ma.uuid, ma.name,
                            self._get_categories(ma.categories),
                            ma.capacity)
                      for ma in model_aisles]
            return aisles

    def get_aisle(self, aisle_id):
        aisles = self.get_aisles()
        aisle = [a for a in aisles if a.id == aisle_id]
        if len(aisle) != 1:
            raise ValueError("couldn't find aisle for this id")
        return aisle[0]

    def get_store_aisles(self, store_id):
        aisle_ids = self.get_store_aisle_ids(store_id)
        with Session(self.engine) as session, session.begin():
            query = session.query(models.Aisle). \
                filter(models.Aisle.uuid.in_(aisle_ids))
            model_aisles = query.all()
            aisles = [Aisle(ma.uuid, ma.name,
                            self._get_categories(ma.categories),
                            ma.capacity)
                      for ma in model_aisles]
            return aisles

    def get_store_aisle_ids(self, store_id):
        with Session(self.engine) as session, session.begin():
            query = session.query(models.StoreAisle). \
                filter(models.StoreAisle.store_uuid == store_id)
            store_aisles = query.all()
            return [sa.aisle_uuid for sa in store_aisles]

    def add_aisle(self, store_id, aisle):
        if aisle.id in [a.id for a in self.get_aisles()]:
            raise ValueError("unable to add new aisle, id already present")
        with Session(self.engine) as session, session.begin():
            sorted_values = sorted(str(c.value) for c in aisle.categories)
            categories_str = ','.join(sorted_values)
            model_aisle = models.Aisle(
                uuid=aisle.id,
                name=aisle.name,
                categories=categories_str,
                capacity=aisle.capacity,
            )
            model_store_aisle = models.StoreAisle(
                store_uuid=store_id,
                aisle_uuid=aisle.id,
            )
            session.add(model_aisle)
            session.add(model_store_aisle)

    def remove_aisle(self, aisle_id):
        if aisle_id not in [a.id for a in self.get_aisles()]:
            raise ValueError("unable to remove aisle, id not present")
        with Session(self.engine) as session, session.begin():
            session.query(models.Aisle). \
                filter(models.Aisle.uuid == aisle_id).delete()
            session.query(models.StoreAisle). \
                filter(models.StoreAisle.aisle_uuid == aisle_id).delete()

    def update_aisle(self, aisle):
        if aisle.id not in [a.id for a in self.get_aisles()]:
            raise ValueError("unable to update aisle, id not present")
        with Session(self.engine) as session, session.begin():
            sorted_values = sorted(str(c.value) for c in aisle.categories)
            categories_str = ','.join(sorted_values)
            query = session.query(models.Aisle). \
                filter(models.Aisle.uuid == aisle.id)
            query.update({
                models.Aisle.name: aisle.name,
                models.Aisle.categories: categories_str,
                models.Aisle.capacity: aisle.capacity,
            })
