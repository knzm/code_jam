#!/usr/bin/env python
# -*- coding: utf-8 -*-

directions = {
    "N": (0, +1),
    "S": (0, -1),
    "E": (+1, 0),
    "W": (-1, 0),
    }

def read(f):
    t = int(f.readline())
    for i in xrange(t):
        x, y = map(int, f.readline().strip().split())
        yield x, y

def solve1(tx, ty):
    memory = {}
    q = [(0, 0, "")]
    while True:
        x, y, s = q.pop(0)
        # print x, y, s
        if (x, y) == (tx, ty):
            return s
        if (x, y) in memory and memory[(x, y)] < len(s):
            continue
        memory[(x, y)] = len(s)
        r = len(s) + 1
        for c, (dx, dy) in directions.items():
            q.append((x + r * dx, y + r * dy, s + c))

def solve(tx, ty):
    s = ""
    if tx > 0:
        s += "WE" * tx
    else:
        s += "EW" * (-tx)
    if ty > 0:
        s += "SN" * ty
    else:
        s += "NS" * (-ty)
    return s

def main(f):
    for i, (x, y) in enumerate(read(f)):
        s = solve(x, y)
        print "Case #%d: %s" % (i+1, s)

_input = """
2
3 4
-3 4
""".strip()

_output = """
Case #1: WNSEN
Case #2: ENSWN
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
