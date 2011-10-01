#!/usr/bin/env python
# -*- coding: utf-8 -*-

def read(f):
    t = int(f.next())
    for i in xrange(t):
        n, pd, pg = map(int, f.next().strip().split())
        yield n, pd, pg

def gcd(p, q):
    assert p > 0 and q > 0
    while p != q:
        if p > q:
            p, q = q, p
        q = q - p
    return p

def check(n, pd, pg):
    if pd > 0:
        factor = gcd(pd, 100)
        today_base_win = pd / factor
        today_base_total = 100 / factor
    else:
        today_base_win = 0
        today_base_total = 1
    if today_base_win > 0 and pg == 0:
        return False
    if today_base_total > today_base_win and pg == 100:
        return False
    for d in xrange(today_base_total, n + 1, today_base_total):
        today_win = d * pd / 100
        today_lost = d - today_win
        if pg > 0:
            factor = gcd(pg, 100)
            base_win = pg / factor
            base_lost = 100 / factor - base_win
        else:
            base_win = 0
            base_lost = 1
        if today_win > 0 and base_win == 0:
            continue
        if today_lost > 0 and base_lost == 0:
            continue
        return True
    else:
        return False

def main(f):
    for i, (n, pd, pg) in enumerate(read(f)):
        # print n, pd, pg
        if check(n, pd, pg):
            print "Case #%d: Possible" % (i + 1)
        else:
            print "Case #%d: Broken" % (i + 1)

_input = """
3
1 100 50
10 10 100
9 80 56
""".strip()

_output = """
Case #1: Possible
Case #2: Broken
Case #3: Possible
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
