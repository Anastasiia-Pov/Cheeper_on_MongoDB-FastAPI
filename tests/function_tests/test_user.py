import unittest
from src.service.service_for_users import check_username


class TestUsername(unittest.TestCase):
    def test_username_with_no_spaces(self):
        self.assertFalse(check_username("username"), False)

    def test_username_with_spaces(self):
        self.assertTrue(check_username("username with spaces"), True)

    def test_username_with_special_symbols(self):
        self.assertTrue(check_username("username!with@specsym&,"), True)

    def test_username_with_specsym_and_spaces(self):
        self.assertTrue(check_username("username with @ specsym, "), True)

    def test_username_with_underscore(self):
        self.assertFalse(check_username("username_with_underscore"), False)

    def test_username_with_numerals(self):
        self.assertFalse(check_username("username1"), False)
