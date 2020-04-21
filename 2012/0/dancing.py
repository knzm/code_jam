#!/usr/bin/env python
# -*- coding: utf-8 -*-

import bisect

def read(f):
    n = int(f.readline())
    for i in xrange(n):
        row = map(int, f.readline().strip().split())
        n, s, p = row[:3]
        t = row[3:]
        assert len(t) == n
        yield s, p, t

def solve(s, p, t):
    t = sorted(t)
    i = bisect.bisect_left(t, p + max(p - 1, 0) * 2)
    j = bisect.bisect_left(t, p + max(p - 2, 0) * 2)
    return len(t) - i + min(i - j, s)

def main(f):
    for i, (s, p, t) in enumerate(read(f)):
        n = solve(s, p, t)
        print "Case #%d: %d" % (i+1, n)

_input = """
4
3 1 5 15 13 11
3 0 8 23 22 21
2 1 1 8 0
6 2 8 29 20 8 18 18 21
""".strip()

_output = """
Case #1: 3
Case #2: 2
Case #3: 1
Case #4: 3
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
