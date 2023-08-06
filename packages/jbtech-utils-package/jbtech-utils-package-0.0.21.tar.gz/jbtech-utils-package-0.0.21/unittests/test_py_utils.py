""" Unit tests for py_utils package """
from utils_package.py_utils.encryption_tool import encode, decode
from unittest import TestCase


class TestPyUtils(TestCase):
    """ Unit tests for py_utils package """

    def test_encode_decode_string(self):
        """ Test to handle the encoding and decoding of strings
        1. Set test variables
        2. Encode the string
        3. Decode the string
        4. Validate the string has been decoded appropriately
        """
        # 1. Set test variables
        password = b'zE4WVPXUfXYxQUrB'
        string = b'test string to be encrypted, with some special chars :{}.'

        # 2. Encode the string
        encoded_string = encode(password, string)
        self.assertNotEqual(encoded_string, string)

        # 3. Decode the string
        decoded_string = decode(password, encoded_string)

        # 4. Validate the string has been decoded appropriately
        self.assertEqual(string, decoded_string)
