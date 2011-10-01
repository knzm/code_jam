#!/usr/bin/env python
# -*- coding: utf-8 -*-

def read(f):
    t = int(f.readline())
    for i in xrange(t):
        yield int(f.readline())

def choice(n, m):
    """
    choose m items from n
    """
    if n < m:
        return 0
    num = 1
    den = 1
    while m > 0:
        num *= n
        den *= m
        n -= 1
        m -= 1
    return num / den

d = {}

def solve(n, rank):
    if (n, rank) in d:
        return d[(n, rank)]

    # print "solve(%d, %d)" % (n, rank)
    if rank == 1:
        return 1

    count = 0

    # i: numbers between rank and n
    m = n - rank - 1
    r = 1
    for i in xrange(rank - 1):
        r = r * m / i
        m += 1
        # print "i=%d, n=%d, rank=%d, r=%d" % (i, n, rank, r)
        if n - rank >= i:
            count += solve(rank, rank - 1 - i) * r

    d[(n, rank)] = count

    return count

def main(f):
    for i, n in enumerate(read(f)):
        count = 0
        for rank in xrange(1, n):
            count += solve(n, rank)
        print "Case #%d: %d" % (i + 1, count % 100003)

_input = """
2
5
6
""".strip()

_output = """
Case #1: 5
Case #2: 8
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
