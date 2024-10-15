import unittest
from src.service import hash_password


class TestHash(unittest.TestCase):
    password1 = "1TestPassword!"
    hash_password1 = '2aca892c90764de4f571c21b836685fe503e29be8f81697842de1bee5ca9792d'
    password2 = "ValidationCheck12@"
    hash_password2 = '714b1358c3f17a0c04af06dfbb73c5049a2b8b64ec5a76274554aa5e5db5d46f'

    def test_hash_password_1(self):
        # Test a valid password (no errors expected)
        self.assertEqual(hash_password(self.password1), self.hash_password1)

    def test_hash_password_2(self):
        # Test a valid password (no errors expected)
        self.assertEqual(hash_password(self.password2), self.hash_password2)
