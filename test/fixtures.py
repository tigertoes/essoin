import glob
import unittest

from test import load_fixture, EssoinTest


class FixturesTest(EssoinTest):

    def test_all(self):
        for fixture in glob.glob('fixtures/*.sdp'):
            fixture = load_fixture(fixture)
            self.essoin.parse(fixture)

