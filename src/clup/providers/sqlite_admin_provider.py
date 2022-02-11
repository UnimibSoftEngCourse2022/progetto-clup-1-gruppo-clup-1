from sqlalchemy.orm import Session

from src.clup.database import Admin, engine, StoreAdmin
from src.clup.entities import admin


class SqliteAdminProvider:
    def get_admins(self):
        db_session = Session(engine)
        admins = db_session.query(Admin).all()
        admins_ent = []
        for a in admins:
            admin_ent = admin.Admin(id=a.uuid, username=a.username, password=a.password)
            admins_ent.append(admin_ent)
        return admins_ent

    def get_admin(self, admin_id):
        db_session = Session(engine)
        admin_db = db_session.query(Admin).filter(Admin.uuid == admin_id).all()[0]
        return admin.Admin(id=admin_db.uuid, username=admin_db.username, password=admin_db.password)

    def add_admin(self, admin_ent):
        db_session = Session(engine)
        new_admin = Admin(uuid=admin_ent.id, username=admin_ent.username, password=admin_ent.password)
        db_session.add(new_admin)
        db_session.commit()

    def remove_admin(self, admin_id):
        db_session = Session(engine)
        db_session.query(Admin).filter(Admin.uuid == admin_id).delete()
        db_session.commit()

    def update_admin(self, admin_ent):
        db_session = Session(engine)
        db_session.query(Admin).filter(Admin.uuid == admin_ent.id).update(
            {Admin.username: admin_ent.username, Admin.password: admin_ent.password}
        )
        db_session.commit()

    def get_store_id(self, admin_id):
        db_session = Session(engine)
        return db_session.query(StoreAdmin.store_uuid).filter(StoreAdmin.admin_uuid == admin_id)[0]


ap = SqliteAdminProvider()
print(ap.get_admins())
ap.add_admin(admin.Admin(11, 'admin1', 'password1'))
ap.add_admin(admin.Admin(12, 'admin2', 'password2'))
print(ap.get_admins())
print(ap.get_admin(11))
ap.remove_admin(11)
print(ap.get_admins())
ap.update_admin(admin.Admin(12, 'admin2 updated', 'password2 updated'))
print(ap.get_admins())
ap.remove_admin(12)
print(ap.get_admins())
