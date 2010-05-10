def read(f):
    t = int(f.readline())
    for i in xrange(t):
        data = f.readline().strip().split()
        n = int(data[0])
        yield map(int, data[1:n+1])

def lcd(seq):
    seq = sorted(seq)
    while len(seq) > 1:
        if seq[0] == 0:
            seq.pop(0)
            continue
        seq = sorted([n % seq[0] for n in seq[1:]] + seq[:1])
    return seq[0]

def main(f):
    for i, ts in enumerate(read(f)):
        seq = sorted(ts)
        seq = sorted([n - seq[0] for n in seq[1:]])
        period = lcd(seq)
        elapsed = ts[0] % period
        if elapsed == 0:
            remaining = 0
        else:
            remaining = period - elapsed
        print "Case #%d:" % (i + 1), remaining

_input = """
3
3 26000000 11000000 6000000
3 1 10 11
2 800000000000000000001 900000000000000000001
""".strip()

_output = """
Case #1: 4000000
Case #2: 0
Case #3: 99999999999999999999
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
    # test_main(True)
    import sys
    if len(sys.argv) > 1:
        f = open(sys.argv[1])
        main(f)
        f.close()
    else:
        main(sys.stdin)
