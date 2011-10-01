#!/usr/bin/env python
# -*- coding: utf-8 -*-

def read(f):
    t = int(f.next())
    for i in xrange(t):
        r, c, d = map(int, f.next().strip().split())
        w = []
        for j in xrange(r):
            w.append(map(int, list(f.next().strip())))
        yield r, c, d, w

def get_weight(w, sx, sy, ex, ey):
    print (sx, sy, ex, ey), ex - sx, ey - sy
    weight = 0
    for y in xrange(sy, ey):
        for x in xrange(sx, ex):
            weight += w[y][x]
    return weight

def main(f):
    for r, c, d, w in read(f):
        print r, c, d, w
        hc = c / 2
        hr = r / 2
        north = get_weight(w, 0, 0, c, hr)
        south = get_weight(w, 0, r - hr, c, r)
        west = get_weight(w, 0, 0, hc, r)
        east = get_weight(w, c - hc, 0, c, r)
        print north, south, west, east

_input = """
2
6 7 2
1111111
1122271
1211521
1329131
1242121
1122211
3 3 7
123
234
345
""".strip()

_output = """
Case #1: 5
Case #2: IMPOSSIBLE
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
    test = True
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
