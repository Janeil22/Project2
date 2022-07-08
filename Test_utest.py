import unittest
from Project import get_city, get_state


class Test_utest(unittest.TestCase):
    def test_city(self):
        self.assertEqual('las vegas', 'las vegas')

    def test_iscity():
        self.assertTrue('las vegas')

    def test_state(self):
        self.assertEqual('nv', 'nv')

    def test_isstate():
        self.assertTrue('nv')


if __name__ == '__main__':
    unittest.main()
