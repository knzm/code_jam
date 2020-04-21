#!/usr/bin/env python
# -*- coding: utf-8 -*-

def read(f):
    n = int(f.readline())
    for i in xrange(n):
        a, b = map(int, f.readline().strip().split())
        yield a, b

def rotate(x, w):
    results = set()
    digits = str(x)
    for i in xrange(1, w):
        results.add(int(digits[i:] + digits[:i], 10))
    return results

def solve_slow(a, b):
    digits_a = str(a)
    digits_b = str(b)
    assert len(digits_a) == len(digits_b)
    w = len(digits_a)
    count = 0
    for i in xrange(a, b):
        for r in rotate(i, w):
            if i < r <= b:
                count += 1
    return count

def main(f):
    for i, (a, b) in enumerate(read(f)):
        n = solve_slow(a, b)
        print "Case #%d: %d" % (i+1, n)

_input = """
4
1 9
10 40
100 500
1111 2222
""".strip()

_output = """
Case #1: 0
Case #2: 3
Case #3: 156
Case #4: 287
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
