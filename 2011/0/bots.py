#!/usr/bin/env python

def read(f):
    t = int(f.next())
    for i in xrange(t):
        seq = []
        elems = f.next().strip().split()
        n = int(elems[0])
        for j in xrange(n):
            seq.append((elems[j*2+1], int(elems[j*2+2])))
        yield seq

def main(f):
    for i, seq in enumerate(read(f)):
        pos = {"O": 1, "B": 1}
        t = 0
        turn = None
        queue = []
        for r, p in seq:
            if turn is None:
                turn = r
            delta = abs(pos[r] - p)
            # print r, pos[r], p, delta
            pos[r] = p
            if turn == r:
                queue.append(delta + 1)
            else:
                dt = sum(queue)
                t += dt
                # print "t=", t, "push", turn, queue
                queue = []
                turn = r
                delta = max(delta - dt, 0)
                queue.append(delta + 1)
        if queue:
            dt = sum(queue)
            t += dt
            # print "t=", t, "push", turn, queue
        print "Case #%d: %d" % (i + 1, t)
        # print

_input = """
3
4 O 2 B 1 B 2 O 4
3 O 5 O 8 B 100
2 B 2 B 1
""".strip()

_output = """
Case #1: 6
Case #2: 100
Case #3: 4
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
