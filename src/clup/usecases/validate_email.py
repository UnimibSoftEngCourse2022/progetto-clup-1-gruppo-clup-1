import re


class ValidateEmail:
    def __init__(self):
        self.mail_regex = r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'
        self.compiled = re.compile(self.mail_regex)

    def execute(self, mail):
        if re.fullmatch(self.compiled, mail):
            return True
        else:
            return False
