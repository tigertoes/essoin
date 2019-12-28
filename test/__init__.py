import os
import unittest
from essoin import Essoin

PATH = os.path.dirname(os.path.realpath(__file__))


class EssoinTest(unittest.TestCase):
    def setUp(self):
        self.essoin = Essoin()


def load_fixture(fixture):
    with open(os.path.join(PATH, fixture)) as fixture_data:
        return fixture_data.read()

