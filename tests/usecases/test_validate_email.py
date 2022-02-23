import unittest

from src.clup.usecases.validate_email import ValidateEmail


class TestValidateEmail(unittest.TestCase):
    def setUp(self):
        self.u = ValidateEmail()

    def test_true_on_valid_emails(self):
        mail1 = 'name.surname@gmail.com'
        mail2 = 'name123@gmail.co.uk'
        mail3 = 'n.cognome12@campus.unimib.it'

        mail1_is_valid = self.u.execute(mail1)
        mail2_is_valid = self.u.execute(mail2)
        mail3_is_valid = self.u.execute(mail3)

        self.assertTrue(mail1_is_valid)
        self.assertTrue(mail2_is_valid)
        self.assertTrue(mail3_is_valid)

    def test_false_on_invalid_emails(self):
        mail1 = 'cicciopasticcio@gmail'
        mail2 = 'mipiaccionoipuntini@...co.uk'
        mail3 = 'n.cognome12@campus.unimib.'

        mail1_is_valid = self.u.execute(mail1)
        mail2_is_valid = self.u.execute(mail2)
        mail3_is_valid = self.u.execute(mail3)

        self.assertFalse(mail1_is_valid)
        self.assertFalse(mail2_is_valid)
        self.assertFalse(mail3_is_valid)
