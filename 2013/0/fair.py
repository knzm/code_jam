#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math

def read(f):
    n = int(f.readline().strip())
    for i in xrange(n):
        a, b = map(int, f.readline().strip().split())
        yield a, b

def generate_palindrome_candidates(a, b):
    a_str = str(a)
    b_str = str(b)

    for digit in xrange(len(a_str), len(b_str) + 1):
        if len(a_str) == digit:
            start = a_str
        else:
            start = "1" + ("0" * (digit - 1))
        if len(b_str) == digit:
            end = b_str
        else:
            end = "9" * digit

        if digit == 1:
            for n in xrange(int(start), int(end) + 1):
                yield n
            continue

        _range = (int(start[:digit / 2]), int(end[:digit / 2]) + 1)
        # prefixes = xrange(int(start[:digit / 2]), int(end[:digit / 2]) + 1)
        if digit % 2 == 0:
            p = _range[0]
            while p < _range[1]:
                yield int(str(p) + str(p)[::-1])
                p += 1
        else:
            p = _range[0]
            while p < _range[1]:
                for i in xrange(10):
                    yield int(str(p) + str(i) + str(p)[::-1])
                p += 1

def search_palindromes(a, b):
    for n in generate_palindrome_candidates(a, b):
        if a <= n <= b:
            yield n

def __count_palindromes(a, b):
    a_str = str(a)
    b_str = str(b)

    count = 0
    for digit in xrange(len(a_str), len(b_str) + 1):
        is_subset = False
        if len(a_str) == digit:
            start = a_str
            is_subset = True
        else:
            start = "1" + ("0" * (digit - 1))
        if len(b_str) == digit:
            end = b_str
            is_subset = True
        else:
            end = "9" * digit

        if digit == 1:
            count += end - start + 1
            continue

        prefixes = range(int(start[:digit / 2]), int(end[:digit / 2]) + 1)
        if digit % 2 == 0:
            if is_subset:
                count += len(prefixes)
                continue
            for p in prefixes:
                if a <= int(str(p) + str(p)[::-1]) <= b:
                    count += 1
        else:
            if is_subset:
                count += len(prefixes) * 10
                continue
            for p in prefixes:
                for i in xrange(10):
                    if a <= int(str(p) + str(i) + str(p)[::-1]) <= b:
                        count += 1

def is_palindrome(n):
    if n < 0:
        return False
    s = str(n)
    d = int(len(s) / 2)
    return s[:d] == s[:-d-1:-1]

def search(a, b):
    for x in search_palindromes(int(math.sqrt(a)), int(math.sqrt(b)) + 1):
        n = x * x
        if not (a <= n <= b):
            continue
        if is_palindrome(n):
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
