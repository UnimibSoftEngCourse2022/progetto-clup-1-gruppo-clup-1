import unittest

from src.clup.usecases.user_login_usecase import UserLoginUseCase


class MockUserProvider:
    def __init__(self):
        self.users = ()

    def set_users(self, users):
        self.users = users

    def get_users(self):
        return self.users

