from dataclasses import replace

from werkzeug.security import generate_password_hash, check_password_hash

from src.clup.entities.exceptions import AuthError


class ChangePassword:
    def __init__(self, user_provider, admin_provider, store_manager_provider):
        self.user_provider = user_provider
        self.admin_provider = admin_provider
        self.store_manager_provider = store_manager_provider

    def execute(self, account_id, old_password, new_password):
        if not new_password:
            raise ValueError('new password is either none or empty')
        try:
            usr = self.user_provider.get_user(account_id)
            self._check_old_password(usr, old_password)
            self._update_account(usr, new_password, self.user_provider)
        except ValueError:
            try:
                admin = self.admin_provider.get_admin(account_id)
                self._check_old_password(admin, old_password)
                self._update_account(admin, new_password, self.admin_provider)
            except ValueError:
                try:
                    store_manager = self.store_manager_provider.get_manager(account_id)
                    self._check_old_password(store_manager, old_password)
                    self._update_account(store_manager, new_password, self.store_manager_provider)
                except ValueError:
                    raise ValueError('unexistent account id')

    def _check_old_password(self, account, old_password):
        if not check_password_hash(account.password_hash, old_password):
            raise AuthError('wrong old password')

    def _update_account(self, account, new_password, provider):
        new_pwd_hash = generate_password_hash(new_password)
        new_account = replace(account, password_hash=new_pwd_hash)
        provider.update(new_account)
