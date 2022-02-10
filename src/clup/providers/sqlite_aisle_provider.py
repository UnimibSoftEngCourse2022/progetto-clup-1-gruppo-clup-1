from sqlalchemy.orm import Session

from src.clup.database import Aisle, engine
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


ap = SqliteAisleProvider()
print(ap.get_aisles())
