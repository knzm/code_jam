#!/usr/bin/env python
# -*- coding: utf-8 -*-

def read(f):
    n = int(f.readline())
    for i in xrange(n):
        a, b = map(int, f.readline().strip().split())
        ps = map(float, f.readline().strip().split())
        assert len(ps) == a
        yield b, ps

def solve(b, ps):
    # print "b =", b, ", ps =", ps
    prob_correct = [None] * (len(ps) + 1)
    prob_correct[0] = 1.0
    for i, p in enumerate(ps):
        prob_correct[i+1] = prob_correct[i] * p

    # print "prob_correct =", prob_correct

    expects = []

    # press backspace key i times
    for i in xrange(len(ps) + 1):
        ex = 2 * (b + i + 1) - len(ps) - (b + 1) * prob_correct[-1-i]
        # print i, ex
        expects.append(ex)
    # retry
    ex = 1 + b + 1
    # print -1, ex
    expects.append(ex)
    return min(expects)

def main(f):
    for i, (b, ps) in enumerate(read(f)):
        p = solve(b, ps)
        print "Case #%d: %.6f" % (i+1, p)

_input = """
3
2 5
0.6 0.6
1 20
1
3 4
1 0.9 0.1
""".strip()

_output = """
Case #1: 7.000000
Case #2: 20.000000
Case #3: 4.500000
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
