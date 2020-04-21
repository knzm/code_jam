#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

def read(f):
    t = int(f.readline())
    for i in xrange(t):
        s, n = f.readline().strip().split()
        yield s, int(n)

def search_consonants(n, s):
    start = None
    for i, c in enumerate(s):
        if c not in "aeiou":
            if start is None:
                start = i
        else:
            if start is not None:
                if i - start >= n:
                    yield start, i
            start = None
    if start is not None:
        yield start, len(s)

def solve(s, n):
    count = 0
    beginning = 0
    for start, end in search_consonants(n, s):
        rest = end - (start + n)
        # print start, end
        for i in xrange(rest + 1):
            left = start + i - beginning
            right = len(s) - (start + n + i)
            # print " ", left, right, (left + 1) * (right + 1)
            count += (left + 1) * (right + 1)
            beginning = start + i + 1
    return count

def main(f):
    for i, (s, n) in enumerate(read(f)):
        p = solve(s, n)
        print "Case #%d: %d" % (i+1, p)

_input = """
4
quartz 3
straight 3
gcj 2
tsetse 2
""".strip()

_output = """
Case #1: 4
Case #2: 11
Case #3: 3
Case #4: 11
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
