import unittest

class TestReception(unittest.TestCase):
    def test_increment(self):
        self.assertEqual(inc_dec.increment(3), 4)

if __name__ == '__main__':
    unittest.main()