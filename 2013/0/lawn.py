#!/usr/bin/env python
# -*- coding: utf-8 -*-

def read(f):
    n = int(f.readline().strip())
    for i in xrange(n):
        n, m = map(int, f.readline().strip().split())
        yield [map(int, f.readline().strip().split()) for j in xrange(n)]

def solve(pattern):
    n = len(pattern)
    m = len(pattern[0])
    field = [([100] * m) for i in xrange(n)]
    for i, row in enumerate(pattern):
        h = max(row)
        for j in xrange(m):
            if field[i][j] > h:
                field[i][j] = h
    for i, col in enumerate(zip(*pattern)):
        h = max(col)
        for j in xrange(n):
            if field[j][i] > h:
                field[j][i] = h
    return field == pattern

def main(f):
    for i, pattern in enumerate(read(f)):
        result = solve(pattern)
        print "Case #%d: %s" % (i+1, ["NO", "YES"][result])

_input = """
3
3 3
2 1 2
1 1 1
2 1 2
5 5
2 2 2 2 2
2 1 1 1 2
2 1 2 1 2
2 1 1 1 2
2 2 2 2 2
1 3
1 2 1
""".strip()

_output = """
Case #1: YES
Case #2: NO
Case #3: YES
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
