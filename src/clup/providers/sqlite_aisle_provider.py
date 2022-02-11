from sqlalchemy.orm import Session

from src.clup.database import Aisle, engine, StoreAisle
from src.clup.entities import aisle
from src.clup.entities.category import Category


class SqliteAisleProvider:
    def get_aisles(self):
        db_session = Session(engine)
        query = db_session.query(Aisle.uuid, Aisle.name, Aisle.categories)
        aisles = query.all()
        aisles_list = []
        for a in aisles:
            cat_str = a.categories
            cat_enum = [Category(int(c)) for c in cat_str.split(',')]
            aisle_entity = aisle.Aisle(id=a.uuid, name=a.name, categories=cat_enum)
            aisles_list.append(aisle_entity)
        return aisles_list

    def get_store_aisles(self, store_id):
        db_session = Session(engine)
        aisles_id = db_session.query(StoreAisle.aisle_uuid).filter(StoreAisle.store_uuid == store_id).all()
        aisles_id = [el[0] for el in aisles_id]
        aisles = []
        for a_id in aisles_id:
            aisle_db = db_session.query(Aisle.uuid, Aisle.name, Aisle.categories).filter(Aisle.uuid == a_id).all()[0]
            aisle_categories_db = aisle_db.categories
            aisle_categories_enum = [Category(int(c)) for c in aisle_categories_db.split(',')]
            aisle_ent = aisle.Aisle(id=aisle_db.uuid, name=aisle_db.name, categories=aisle_categories_enum)
            aisles.append(aisle_ent)
        return aisles

    def get_store_aisles_id(self, store_id):
        aisles = self.get_store_aisles(store_id)
        return [a.id for a in aisles]

    def get_aisle(self, aisle_id):
        db_session = Session(engine)
        aisle_db = db_session.query(Aisle.uuid, Aisle.name, Aisle.categories).filter(Aisle.uuid == aisle_id).all()[0]
        aisle_db_categories = aisle_db.categories
        aisle_cat_enum = [Category(int(c)) for c in aisle_db_categories.split(',')]
        return aisle.Aisle(id=aisle_db.uuid, name=aisle_db.name, categories=aisle_cat_enum)

    def add_aisle(self, store_id, aisle_ent):
        db_session = Session(engine)
        categories_str = ','.join([f'{e.value}' for e in aisle_ent.categories])
        new_aisle = Aisle(uuid=aisle_ent.id, name=aisle_ent.name, categories=categories_str)
        db_session.add(new_aisle)
        new_aisle_store = StoreAisle(store_uuid=store_id, aisle_uuid=aisle_ent.id)
        db_session.add(new_aisle_store)
        db_session.commit()

    def remove_aisle(self, aisle_id):
        db_session = Session(engine)
        db_session.query(Aisle).filter(Aisle.uuid == aisle_id).delete()
        db_session.query(StoreAisle).filter(StoreAisle.aisle_uuid == aisle_id).delete()
        db_session.commit()

    def update_aisle(self, aisle_ent):
        db_session = Session(engine)
        db_session.query(Aisle).filter(Aisle.uuid == aisle_ent.id).update(
            {Aisle.name: aisle_ent.name, Aisle.categories: Aisle.categories}
        )
        db_session.commit()


ap = SqliteAisleProvider()

print(ap.get_aisles())
print(ap.get_store_aisles(100))
print(ap.get_store_aisles_id(100))
print(ap.get_aisle(10))
ap.add_aisle(100, aisle.Aisle(id=40, name='aisle4', categories=[Category.FISH, Category.FRUIT]))
print(ap.get_store_aisles(100))
ap.remove_aisle(40)
print(ap.get_aisles())
ap.update_aisle(aisle.Aisle(10, 'updated_aisle', categories=[Category.FISH, Category.FRUIT]))
print(ap.get_aisles())
