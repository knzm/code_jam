#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import defaultdict

def read(f):
    t = int(f.readline())
    for i in xrange(t):
        e, r, n = map(int, f.readline().strip().split())
        vs = map(int, f.readline().strip().split())
        assert len(vs) == n
        yield e, r, vs

def solve(energy, regain, values):
    table = defaultdict(int)
    table[energy] = 0

    for i, value in enumerate(values):
        next_table = defaultdict(int)
        for e, g in table.items():
            for i in xrange(e + 1):
                next_energy = min(e - i + regain, energy)
                next_value = g + value * i
                if next_table[next_energy] < next_value:
                    next_table[next_energy] = next_value
        table = next_table

    return max(table.values())


def main(f):
    for i, (e, r, vs) in enumerate(read(f)):
        p = solve(e, r, vs)
        print "Case #%d: %d" % (i+1, p)

_input = """
3
5 2 2
2 1
5 2 2
1 2
3 3 4
4 1 3 5
""".strip()

_output = """
Case #1: 12
Case #2: 12
Case #3: 39
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
