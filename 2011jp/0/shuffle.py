#!/usr/bin/env python
# -*- coding: utf-8 -*-

import itertools

def read(f):
    t = int(f.readline())
    for i in xrange(t):
        m, c, w = map(int, f.readline().strip().split())
        cuts = []
        for j in xrange(c):
            a, b = map(int, f.readline().strip().split())
            cuts.append((a, b))
        yield m, w, cuts

def simple_solve(m, w, cuts):
    cards = range(1, m+1)
    for a, b in cuts:
        cards = cards[a-1:a+b-1] + cards[:a-1] + cards[a+b-1:]
    return cards[w-1]


class Chunk(object):
    def __init__(self, start, stop):
        self.start = start
        self.stop = stop

    def __len__(self):
        return self.stop - self.start

    def __getitem__(self, key):
        if isinstance(key, slice):
            start, stop, stride = key.indices(len(self))
            if stride != 1:
                raise ValueError("stride unsupported")
            return Chunk(self.start + start, self.start + stop)
        else:
            i = int(key)
            if i >= len(self):
                raise IndexError
            if i < 0:
                i += len(self)
            return self.start + i

    def __iter__(self):
        return iter(xrange(self.start, self.stop))

    def __repr__(self):
        return "<Chunk %r>" % ((self.start, self.stop),)


class Cards(object):
    def __init__(self, m):
        self.chunks = [Chunk(1, m+1)]

    def __len__(self):
        return sum(map(len, self.chunks))

    def __getitem__(self, key):
        i = int(key)
        chunk_index, chunk_offset = self._find_chunk(i)
        return self.chunks[chunk_index][chunk_offset]

    def _find_chunk(self, offset):
        for i, chunk in enumerate(self.chunks):
            n = len(chunk)
            if offset < n:
                return i, offset
            offset -= n
        raise IndexError

    def cut(self, a, b):
        chunk_index_a, chunk_offset_a = self._find_chunk(a-1)
        chunk_index_b, chunk_offset_b = self._find_chunk(a+b-2)

        if chunk_index_a == chunk_index_b:
            chunk = self.chunks[chunk_index_a]

            chunks = (
                [chunk[chunk_offset_a:chunk_offset_b+1]],
                self.chunks[:chunk_index_a] + [chunk[:chunk_offset_a]],
                [chunk[chunk_offset_b+1:]] + self.chunks[chunk_index_a+1:],
                )
        else:
            chunk_a = self.chunks[chunk_index_a]
            chunk_b = self.chunks[chunk_index_b]

            chunks = (
                ([chunk_a[chunk_offset_a:]] +
                 self.chunks[chunk_index_a+1:chunk_index_b] +
                 [chunk_b[:chunk_offset_b+1]]),
                self.chunks[:chunk_index_a] + [chunk_a[:chunk_offset_a]],
                [chunk_b[chunk_offset_b+1:]] + self.chunks[chunk_index_b+1:],
                )

        assert sum(map(len, chunks[0])) == b
        assert sum(map(len, chunks[1])) == a - 1
        assert sum(map(len, chunks[2])) == len(self) - a - b + 1

        cards = Cards(0)
        cards.chunks = [chunk for chunk in itertools.chain(*chunks)
                        if len(chunk) > 0]
        assert len(cards) == len(self)
        return cards

    def flatten(self):
        return map(tuple, self.chunks)

    def __iter__(self):
        return itertools.chain(*self.chunks)

    def __repr__(self):
        return "<Cards %r>" % self.chunks


def solve(m, w, cuts):
    # print "m =", m
    cards = Cards(m)
    if len(cards) != m:
        import pdb; pdb.set_trace()
    assert len(cards) == m
    # print list(cards)
    for a, b in cuts:
        # print "a, b =", a, b
        cards = cards.cut(a, b)
        if len(cards) != m:
            import pdb; pdb.set_trace()
        assert len(cards) == m
        # print list(cards)
    return cards[w-1]

def main(f):
    for i, (m ,w, cuts) in enumerate(read(f)):
        card = solve(m, w, cuts)
        print "Case #%d: %d" % (i + 1, card)

_input = """
3
1 1 1
1 1
2 3 1
2 1
2 1
2 1
5 3 2
4 2
5 1
4 2
""".strip()

_output = """
Case #1: 1
Case #2: 2
Case #3: 2
""".strip()

def test_main(compare=False):
    import sys
    from difflib import unified_diff
    from StringIO import StringIO

    if compare:
        stdout = sys.stdout
        sys.stdout = StringIO()
        try:
            main(StringIO(_input))
            result = sys.stdout.getvalue().strip()
        finally:
            sys.stdout = stdout

        print result

        for line in unified_diff(result.splitlines(), _output.splitlines(),
                                 'Output', 'Expect', lineterm=''):
            print line

        if result == _output:
            print "OK"
        else:
            print "NG"

    else:
        main(StringIO(_input))

if __name__ == '__main__':
    test = False
    compare = False
    if test:
        test_main(compare)
    else:
        import sys
        if len(sys.argv) > 1:
            f = open(sys.argv[1])
            main(f)
            f.close()
        else:
            main(sys.stdin)
