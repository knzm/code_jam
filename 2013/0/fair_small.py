#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math

def read(f):
    n = int(f.readline().strip())
    for i in xrange(n):
        a, b = map(int, f.readline().strip().split())
        yield a, b

def is_palindrome(n):
    if n < 0:
        return False
    s = str(n)
    d = int(len(s) / 2)
    return s[:d] == s[:-d-1:-1]

def search(a, b):
    for x in xrange(int(math.sqrt(a)), int(math.sqrt(b)) + 1):
        n = x * x
        if not (a <= n <= b):
            continue
        if is_palindrome(x) and is_palindrome(n):
            yield n

def solve(a, b):
    n = 0
    for x in search(a, b):
        # print x
        n += 1
    return n

def main(f):
    for i, (a, b) in enumerate(read(f)):
        p = solve(a, b)
        print "Case #%d: %d" % (i+1, p)

_input = """
3
1 4
10 120
100 1000
""".strip()

_output = """
Case #1: 2
Case #2: 0
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
