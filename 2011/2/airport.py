#!/usr/bin/env python
# -*- coding: utf-8 -*-

def read(f):
    T = int(f.next())
    for i in xrange(T):
        X, S, R, t, N = map(int, f.next().strip().split())
        walkways = []
        for j in xrange(N):
            B, E, w = map(int, f.next().strip().split())
            walkways.append((B, E, w))
        yield X, S, R, t, walkways

def main(f):
    for X, S, R, t, walkways in read(f):
        # X: length of the corridor
        # S: walking speed
        # R: running speed
        # t: maximum time one can run
        print X, S, R, t, walkways

_input = """
3
10 1 4 1 2
4 6 1
6 9 2
12 1 2 4 1
6 12 1
20 1 3 20 5
0 4 5
4 8 4
8 12 3
12 16 2
16 20 1
""".strip()

_output = """
Case #1: 4.000000
Case #2: 5.500000
Case #3: 3.538095238
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
