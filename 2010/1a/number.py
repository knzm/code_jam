def read(f):
    t = int(f.readline())
    for i in xrange(t):
        a1, a2, b1, b2 = map(int, f.readline().strip().split())
        yield (a1, a2), (b1, b2)

def order(a, b):
    if a < b:
        return b, a
    else:
        return a, b

result = {}

def search(a, b, turn):
    if (a, b) in result:
        if result[(a, b)]:
            return turn
        else:
            return 1 - turn
    for i in reversed(xrange(int(a / b))):
        c = a - b * (i + 1)
        if c <= 0:
            continue
        p, q = order(b, c)
        winner = search(p, q, 1 - turn)
        if winner == turn:
            result[(a, b)] = True
            return turn
    else:
        result[(a, b)] = False
        return 1 - turn

def game(a, b):
    winner = search(a, b, 0)
    return winner == 0

def main(f):
    for i, ((a1, a2), (b1, b2)) in enumerate(read(f)):
        win = 0
        for a in xrange(a1, a2+1):
            for b in xrange(b1, b2+1):
                if game(*order(a, b)):
                    win += 1
        print "Case #%d: %d" % (i+1, win)

_input = """
3
5 5 8 8
11 11 2 2
1 6 1 6
""".strip()

_output = """
Case #1: 0
Case #2: 1
Case #3: 20
""".strip()

def test_main(compare=False):
    import sys
    from difflib import unified_diff
    from StringIO import StringIO

    if not compare:
        main(StringIO(_input))
        return

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
