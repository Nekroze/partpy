import unittest
from partpy.matcher import Matcher


class Test(unittest.TestCase):
    
    def setUp(self):
        self.MAT = Matcher('hello world\ntesting stuff')
    
    def test_match_string(self):
        self.assertEqual(self.MAT.match_string('hello', 1), True)
        self.assertEqual(self.MAT.match_string('hello'), True)
        self.assertEqual(self.MAT.match_string('hel', 1), False)
        self.assertEqual(self.MAT.match_string('hel'), True)
        self.assertEqual(self.MAT.match_string('hello world', 1), False)
        self.assertEqual(self.MAT.match_string('hello world'), True)

if __name__ == "__main__":
    unittest.main()
