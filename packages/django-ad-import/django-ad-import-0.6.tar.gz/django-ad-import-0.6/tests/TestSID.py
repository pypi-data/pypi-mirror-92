import unittest
import ad.sid


class TestSID(unittest.TestCase):
    byte_value = b'\x01\x05\x00\x00\x00\x00\x00\x05\x15\x00\x00\x00\xa3<\x9c\x1e\x8a\x15iT\xa2\x18\x94\xda\xab\x07\x01\x00'
    string_value = 'S-1-5-21-513555619-1416172938-3667138722-67499'

    def test_format_sid(self):
        self.assertEqual(self.string_value, sid.format_sid(self.byte_value))

    def test_parse_sid(self):
        self.assertEqual(self.byte_value, sid.parse_sid(self.string_value))
