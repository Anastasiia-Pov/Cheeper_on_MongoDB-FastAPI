import unittest
from src.service import pass_validation


class TestPassword(unittest.TestCase):
    no_numeral = 'Password should have at least one numeral'
    short_pass = 'Password should have at least 8 characters'
    no_uppercase = 'Password should have at least one uppercase letter'
    no_lowercase = 'Password should have at least one lowercase letter'
    no_special_symbol = 'Password should have at least one of the symbols: ~, !, @, #, $, %, ^, &, *, (, ), _, +, =, -'

    def test_valid_password(self):
        # Test a valid password (no errors expected)
        self.assertIsNone(pass_validation("1TestPassword!"))

    def test_short_password(self):
        # Test a short password (less than 8 characters)
        self.assertIn(self.short_pass, pass_validation("Pass!1"))

    def test_no_numeral(self):
        # Test a password without numerals
        self.assertIn(self.no_numeral, pass_validation("password!@"))

    def test_no_uppercase(self):
        # Test a password without uppercase letters
        self.assertIn(self.no_uppercase, pass_validation("password1@"))

    def test_no_lowercase(self):
        # Test a password without lowercase letters
        self.assertIn(self.no_lowercase, pass_validation("PASSWORD1@"))

    def test_no_special_symbol(self):
        # Test a password without special symbols
        self.assertIn(self.no_special_symbol, pass_validation("1TestPassword"))

    def test_no_spec_symbol_and_numeral(self):
        # Test a password that has two errors
        expected_errors = [
            self.no_numeral,
            self.no_special_symbol
        ]
        self.assertEqual(pass_validation("TestPassword"), expected_errors)

    def test_no_lower_uppercase(self):
        # Test a password that has two errors
        expected_errors = [
            self.no_uppercase,
            self.no_lowercase
        ]
        self.assertEqual(pass_validation("1234567!"), expected_errors)

    def test_lack_numeral_uppercase_spec_symbol(self):
        # Test a password that has two errors
        expected_errors = [
            self.no_numeral,
            self.no_lowercase,
            self.no_special_symbol
        ]
        self.assertEqual(pass_validation("TESTPASSWORD"), expected_errors)

    def test_lack_short_uppercase_numeral(self):
        # Test a password that has two errors
        expected_errors = [
            self.short_pass,
            self.no_numeral,
            self.no_uppercase
        ]
        self.assertEqual(pass_validation("test!"), expected_errors)

    def test_multiple_errors(self):
        # Test a password that has multiple errors
        expected_errors = [
            self.short_pass,
            self.no_numeral,
            self.no_uppercase,
            self.no_special_symbol
        ]
        self.assertEqual(pass_validation("short"), expected_errors)


if __name__ == '__main__':
    unittest.main()
