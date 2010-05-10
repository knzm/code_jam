def read(f):
    t = int(f.readline())
    for i in xrange(t):
        n, k = f.readline().strip().split()
        yield int(n), int(k)

def main(f):
    for i, (n, k) in enumerate(read(f)):
        is_on = ((2 ** n) -1) & (k + 1) == 0
        print "Case #%d: %s" % (i + 1, ["OFF", "ON"][is_on])

_input = """
4
1 0
1 1
4 0
4 47
""".strip()

_output = """
Case #1: OFF
Case #2: ON
Case #3: OFF
Case #4: ON
""".strip()

def test_main():
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

    for line in unified_diff(result.splitlines(), _output.splitlines(),
                             'Output', 'Expect', lineterm=''):
        print line

    if result == _output:
        print "OK"
    else:
        print "NG"

if __name__ == '__main__':
    # test_main()
    import sys
    if len(sys.argv) > 1:
        f = open(sys.argv[1])
        main(f)
        f.close()
    else:
        main(sys.stdin)
