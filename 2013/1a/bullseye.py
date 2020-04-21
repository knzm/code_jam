#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math

def read(f):
    t = int(f.readline())
    for i in xrange(t):
        r, t = map(int, f.readline().strip().split())
        yield r, t

def f(n, r):
    # ((r + 1)^2 - r^2) + ((r + 3)^2 - (r + 2)^2) +
    #  ... + ((r + 2n + 1)^2 - (r + 2n)^2)
    # = (2r + 1) + (2r + 5) + (2r + 9) + ... + (2r + 4n - 3)
    # = 2nr + (1 + 5 + 9 + ... + 4n-3)
    # = 2nr + n(2n-1)
    return 2 * n * r + n * (2 * n - 1)

def solve(r, t):
    # f(n, r) < t
    # n < sqrt((r - 1/2)^2 + 2t) - (r - 1/2)
    n = int((math.sqrt(((r - 0.5) ** 2) + 2 * t) - (r - 0.5)) / 2)
    while f(n, r) > t:
        n -= 1
    return n

def main(f):
    for i, (r, t) in enumerate(read(f)):
        p = solve(r, t)
        print "Case #%d: %d" % (i+1, p)

_input = """
5
1 9
1 10
3 40
1 1000000000000000000
10000000000000000 1000000000000000000
""".strip()

_output = """
Case #1: 1
Case #2: 2
Case #3: 3
Case #4: 707106780
Case #5: 49
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
