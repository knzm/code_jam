import unittest
from shuffle import Chunk, Cards


class TestChunk(unittest.TestCase):
    def test_new(self):
        c = Chunk(1, 11)
        self.assertEquals(c.start, 1)
        self.assertEquals(c.stop, 11)
        self.assertEquals(len(c), 10)

    def test_getitem(self):
        c = Chunk(1, 11)
        self.assertEquals(c[0], 1)
        self.assertEquals(c[9], 10)
        self.assertEquals(c[-1], 10)
        self.assertRaises(IndexError, lambda: c[10])

    def test_getslice_first_half(self):
        c = Chunk(1, 11)[:5]
        self.assertEquals(c.start, 1)
        self.assertEquals(c.stop, 6)

    def test_getslice_second_half(self):
        c = Chunk(1, 11)[5:]
        self.assertEquals(c.start, 6)
        self.assertEquals(c.stop, 11)

    def test_getslice_intermediate(self):
        c = Chunk(1, 11)[1:2]
        self.assertEquals(c.start, 2)
        self.assertEquals(c.stop, 3)

    def test_getslice_overrun(self):
        c = Chunk(1, 11)[2:100]
        self.assertEquals(c.start, 3)
        self.assertEquals(c.stop, 11)

    def test_repr(self):
        c = Chunk(1, 11)
        self.assertEquals(repr(c), "<Chunk (1, 11)>")


class TestCards(unittest.TestCase):
    def test_cut_simple(self):
        cards = Cards(1)
        self.assertEquals(len(cards), 1)
        cards = cards.cut(1, 1)
        self.assertEquals(len(cards), 1)

    def test_cut_complex(self):
        cards = Cards(10)
        cards = cards.cut(6, 5)
        self.assertEquals(len(cards), 10)
        self.assertEquals(len(cards.chunks), 2)
        cards = cards.cut(3, 5)
        self.assertEquals(list(cards), [8, 9, 10, 1, 2, 6, 7, 3, 4, 5])

if __name__ == '__main__':
    unittest.main()
