import unittest
from test import EssoinTest

from essoin import SdpParseException


class ParsingTest(EssoinTest):

    def test_invalid_types(self):
        with self.assertRaises(ValueError):
            self.essoin.parse(6)
            self.essoin.parse(b'\xff\xff')

    def test_invalid_declaration(self):
        with self.assertRaises(SdpParseException):
            self.essoin.parse('5')  # Not lower case letter
            self.essoin.parse('v!') # Second character not '='
            self.essoin.parse('m=') # Not long enough

    def test_invalid_version(self):
        with self.assertRaises(SdpParseException):
            self.essoin.parse('v=1')

    def test_email(self):
        with self.assertRaises(SdpParseException):
            self.essoin.parse('e=[invalid!email]')

    def test_invalid_type(self):
        with self.assertRaises(SdpParseException):
            self.essoin.parse('q=4')

    def test_invalid_nettype(self):
        with self.assertRaises(KeyError):
            self.essoin.parse('c=IN IP1 169.254.0.0/127')

    def test_invalid_time_interval(self):
        with self.assertRaises(SdpParseException):
            self.essoin.parse('r=1w')

    def test_invalid_time_offsets(self):
        with self.assertRaises(SdpParseException):
            self.essoin.parse('z=0 1h 0')

    def test_invalid_attribute(self):
        with self.assertRaises(SdpParseException):
            self.essoin.parse('a=foo:bar:baz')

    def test_time_conversion(self):
        self.assertEqual(self.essoin._convert_time('61s'), 61)
        self.assertEqual(self.essoin._convert_time('7m'), 420)
        self.assertEqual(self.essoin._convert_time('2h'), 7200)
        self.assertEqual(self.essoin._convert_time('1d'), 86400)

