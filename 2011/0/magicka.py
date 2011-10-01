#!/usr/bin/env python

from collections import defaultdict

def read(f):
    t = int(f.next())
    for i in xrange(t):
        elems = f.next().strip().split()
        c = int(elems.pop(0))
        if c > 0:
            combs = elems[0:c]
            del elems[0:c]
            for comb in combs:
                assert len(comb) == 3
        else:
            combs = []
        d = int(elems.pop(0))
        if d > 0:
            opps = elems[0:d]
            del elems[0:d]
            for opp in opps:
                assert len(opp) == 2
        else:
            opps = []
        n = int(elems.pop(0))
        if n > 0:
            invokes = list(elems.pop(0))
            assert len(invokes) == n
        else:
            invokes = []
        assert len(elems) == 0
        yield combs, opps, invokes

def main(f):
    for i, (combs, opps, invokes) in enumerate(read(f)):
        rules = defaultdict(lambda: {"comb": {}, "opp": set()})
        for comb in combs:
            x, y, z = comb
            rules[x]["comb"][y] = z
            rules[y]["comb"][x] = z
        for opp in opps:
            x, y = opp
            rules[x]["opp"].add(y)
            rules[y]["opp"].add(x)
        queue = []
        for elem in invokes:
            rule = rules[elem]
            if len(queue) > 0:
                x = queue[-1]
                if x in rule["comb"]:
                    queue.pop()
                    queue.append(rule["comb"][x])
                    continue
                x = rule["opp"].intersection(queue)
                if x:
                    queue = []
                    continue
            queue.append(elem)
        print "Case #%d: [%s]" % (i + 1, ", ".join(queue))

_input = """
5
0 0 2 EA
1 QRI 0 4 RRQR
1 QFT 1 QF 7 FAQFDFQ
1 EEZ 1 QE 7 QEEEERA
0 1 QW 2 QW
""".strip()

_output = """
Case #1: [E, A]
Case #2: [R, I, R]
Case #3: [F, D, T]
Case #4: [Z, E, R, A]
Case #5: []
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
