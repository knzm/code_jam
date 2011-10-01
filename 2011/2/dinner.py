#!/usr/bin/env python
# -*- coding: utf-8 -*-

import itertools
import math

def read(f):
    t = int(f.next())
    for i in xrange(t):
        yield int(f.next())

def gcd(p, q):
    while True:
        if p == 0:
            return q
        if q == 0:
            return p
        if p < q:
            q = q % p
        else:
            p = p % q

def _ifactorize_p():
    u"""2, 3, および素数の可能性がある奇数 p = 6 * n ± 1"""

    yield 2
    yield 3
    num = 1
    for add in itertools.cycle((4, 2)):
        num += add
        yield num

def ifactorize(num):
    u"""素因数分解

    素因数を小さい順に一つずつ返すイテレータ。"""

    num = int(num)
    if num < 1:
        raise ValueError(u'%d is not positive number' % num)
    elif num == 1:
        yield 1
        return

    for fact in _ifactorize_p():
        if num < fact ** 2:
            if num > 1:
                yield num
            break
        q, r = divmod(num, fact)
        while not r:
            num = q
            yield fact
            q, r = divmod(num, fact)

def factorize(num):
    u"""素因数分解

    素因数をまとめた tuple を返す

    >>> factorize(360)
    (2, 2, 2, 3, 3, 5)
    """
    return tuple(ifactorize(num))


def deform(x, n):
    for i in reversed(xrange(n)):
        p = i + 1
        if x % p == 0:
            return p, x / p


def solve(n):
    factors = []
    x = 1
    for i in xrange(n):
        p = i + 1
        r = gcd(x, p)
        factor = p / r
        x *= factor
        factors += factorize(factor)
    factors1 = [1] + sorted([factor for factor in factors if factor != 1])
    factors2 = []
    while x > 1:
        p, q = deform(x, n)
        x = q
        factors2.append(p)
    if len(factors2) == 0:
        factors2 = [1]
    # print n, factors1, factors2
    return len(factors1) - len(factors2)


def main(f):
    for i, n in enumerate(read(f)):
        y = solve(n)
        print "Case #%d: %d" % (i + 1, y)


_input = """
4
1
3
6
16
""".strip()

_output = """
Case #1: 0
Case #2: 1
Case #3: 2
Case #4: 5
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
