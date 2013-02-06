import unittest
from partpy.sourcestring import SourceString


class Test_SourceString(unittest.TestCase):

    def setUp(self):
        self.SRC = SourceString()
        self.SRC.set_string('hello world')
        self.MLSRC = SourceString()
        self.MLSRC.set_string('hello\nworld')

    def test_has_space(self):
        self.assertEqual(self.SRC.has_space(), True)
        self.assertEqual(self.SRC.has_space(11), True)
        self.assertEqual(self.SRC.has_space(12), False)
        self.SRC.eat_length(11)

        self.assertEqual(self.SRC.has_space(), False)

    def test_eat_string(self):
        self.SRC.eat_string('hello world')
        self.assertEqual(self.SRC.end(), True)
        
    def test_eat_string_multiline_peices(self):
        self.MLSRC.eat_string(self.MLSRC.get_length(5))
        self.assertEqual(self.MLSRC.line(), 0)
        self.assertEqual(self.MLSRC.column(), 5)
        
        self.assertEqual(self.MLSRC.get_char(), '\n')
        self.MLSRC.eat_string(self.MLSRC.get_char())
        self.assertEqual(self.MLSRC.line(), 1)
        self.assertEqual(self.MLSRC.column(), 0)
        
        self.MLSRC.eat_string(self.MLSRC.get_length(5))
        self.assertEqual(self.MLSRC.line(), 1)
        self.assertEqual(self.MLSRC.column(), 5)
        self.assertEqual(self.MLSRC.get_char(), '')
        
    def test_eat_string_multiline_chunk(self):
        self.MLSRC.eat_string('hello\nworld')
        self.assertEqual(self.MLSRC.line(), 1)
        self.assertEqual(self.MLSRC.column(), 5)
        self.assertEqual(self.MLSRC.get_char(), '')
        
    def test_get_length(self):
        self.assertEqual(self.SRC.get_length(5), 'hello')
        self.assertEqual(self.SRC.get_length(11), 'hello world')
        self.assertEqual(self.SRC.get_length(12), '')
        self.assertEqual(self.SRC.get_length(12,  True), 'hello world')

    def test_get_char(self):
        self.assertEqual(self.SRC.get_char(), 'h')
        self.SRC.eat_length(10)
        self.assertEqual(self.SRC.get_char(), 'd')
        self.SRC.eat_length(1)
        self.assertEqual(self.SRC.end(), True)
        self.assertEqual(self.SRC.get_char(), '')
        
    def test_get_string(self):
        self.assertEqual(self.SRC.get_string(), 'hello')
        self.SRC.eat_length(5)
        self.assertEqual(self.SRC.get_string(), '')
        self.SRC.eat_length(1)
        self.assertEqual(self.SRC.get_string(), 'world')
        self.SRC.eat_length(5)
        self.assertEqual(self.SRC.get_string(), '')
        self.SRC.eat_length(5)
        self.assertEqual(self.SRC.end(), True)

if __name__ == "__main__":
    unittest.main()
