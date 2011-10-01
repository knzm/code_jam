#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import namedtuple

class Bag(object):
    def __init__(self, c, t, s):
        self.c = c
        self.t = t
        self.s = s

def read(f):
    t = int(f.readline())
    for i in xrange(t):
        n, k = map(int, f.readline().strip().split())
        bags = []
        for j in xrange(n):
            c, t, s = map(int, f.readline().strip().split())
            bags.append(Bag(c, t, s))
        yield k, bags

def solve(days, bags):
    s = 0
    times = sorted([bag.t for bag in bags])
    for t1, t2 in reversed(zip([0] + times, times)):
        available_bags = filter(lambda bag: bag.c > 0 and t1 < bag.t, bags)
        n = t2 - t1
        for bag in sorted(available_bags, key=lambda bag: bag.s, reverse=True):
            if n < bag.c:
                s += bag.s * n
                bag.c -= n
                break
            else:
                s += bag.s * bag.c
                n -= bag.c
                bag.c = 0
    return s

def main(f):
    for i, (days, bags) in enumerate(read(f)):
        y = solve(days, bags)
        print "Case #%d: %d" % (i+1, y)

_input = """
3
2 3
2 2 2
3 3 1
2 3
1 3 2
1 3 1
5 5
5 5 1
4 4 2
3 3 3
2 2 4
1 1 5
""".strip()

_output = """
Case #1: 5
Case #2: 3
Case #3: 15
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
    compare = True
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
