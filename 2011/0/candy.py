#!/usr/bin/env python

def read(f):
    t = int(f.next())
    for i in xrange(t):
        n = int(f.next())
        yield map(int, f.next().strip().split())

def format_bits(bits):
    digits = []
    while bits > 0:
        digits.append(bits & 1)
        bits >>= 1
    return digits

def main(f):
    for i, candies in enumerate(read(f)):
        bits = 0
        for candy in candies:
            bits ^= candy
        if bits == 0:
            print "Case #%d: %d" % (i + 1, sum(candies) - min(candies))
        else:
            print "Case #%d: NO" % (i + 1)

_input = """
2
5
1 2 3 4 5
3
3 5 6
""".strip()

_output = """
Case #1: NO
Case #2: 11
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
