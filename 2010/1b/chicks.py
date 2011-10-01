#!/usr/bin/env python

def read(f):
    c = int(f.readline())
    for i in xrange(c):
        n, k, b, t = map(int, f.readline().strip().split())
        x_i = map(int, f.readline().strip().split())
        v_i = map(int, f.readline().strip().split())
        yield k, b, t, zip(x_i, v_i)

def main(f):
    for k, b, t, chicks in read(f):
        crosspoint = {}
        for x, v in sorted(chicks):
            arrival = float(b - x) / v

_input = """
3
5 3 10 5
0 2 5 6 7
1 1 1 1 4
5 3 10 5
0 2 3 5 7
2 1 1 1 4
5 3 10 5
0 2 3 4 7
2 1 1 1 4
""".strip()

_output = """
Case #1: 0
Case #2: 2
Case #3: IMPOSSIBLE
""".strip()

def test_main(compare=False):
    import sys
    from difflib import unified_diff
    from StringIO import StringIO

    stdout = sys.stdout
    sys.stdout = StringIO()
    try:
        main(StringIO(_input))
        result = sys.stdout.getvalue().strip()
    finally:
        sys.stdout = stdout

    print result

    if compare:
        for line in unified_diff(result.splitlines(), _output.splitlines(),
                                 'Output', 'Expect', lineterm=''):
            print line

        if result == _output:
            print "OK"
        else:
            print "NG"

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
