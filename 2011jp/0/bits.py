#!/usr/bin/env python
# -*- coding: utf-8 -*-

def read(f):
    t = int(f.readline())
    for i in xrange(t):
        n = int(f.readline())
        yield n

def solve(n):
    bits = map(int, bin(n)[2:])
    for i in reversed(xrange(len(bits))):
        if bits[i] == 0:
            w = i
            break
    else:
        w = 0

    p = sum(bits) + w

    return p

def main(f):
    for i, n in enumerate(read(f)):
        p = solve(n)
        print "Case #%d: %d" % (i+1, p)

_input = """
4
1
4
31
1125899906842624
""".strip()

_output = """
Case #1: 1
Case #2: 3
Case #3: 5
Case #4: 51
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
