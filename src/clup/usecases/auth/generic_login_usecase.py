from werkzeug.security import check_password_hash


class GenericLoginUsecase:
    def __init__(self, admin_provider, user_provider, store_manager_provider):
        self.admin_provider = admin_provider
        self.user_provider = user_provider
        self.store_manager_provider = store_manager_provider

    def execute(self, username, password):
        users = self.user_provider.get_users()
        admins = self.admin_provider.get_admins()
        store_managers = self.store_manager_provider.get_store_managers()

        if username in [u.username for u in users]:
            u_id = self._search_user(username, password, users)
            return u_id, 'user'
        elif username in [u.username for u in admins]:
            u_id = self._search_user(username, password, admins)
            return u_id, 'admin'
        elif username in [u.username for u in store_managers]:
            u_id = self._search_user(username, password, store_managers)
            return u_id, 'store_manager'
        else:
            raise ValueError("wrong credentials")

    def _search_user(self, username, password, accounts):
        for account in accounts:
            if account.username == username:
                if check_password_hash(account.password_hash, password):
                    return account.id
                else:
                    raise ValueError("wrong password")
        raise ValueError("problem while searching for the account")
