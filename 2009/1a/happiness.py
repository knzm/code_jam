answer = {}

def rebase(x, base):
    digits = []
    while x > 0:
        digit = x % base
        digits.append(digit)
        x /= base
    return list(reversed(digits))

def process(x, base):
    n = 0
    for digit in rebase(x, base):
        n += digit ** 2
    return n

def is_happy(x, base):
    # print "is_happy(%d, %d)" % (x, base)
    history = {}
    while x not in history and (x, base) not in answer:
        history[x] = True
        x = process(x, base)
    if (x, base) not in answer:
        answer[(x, base)] = (x == 1)
    return answer[(x, base)]

def solve(bases):
    import itertools
    for x in itertools.count(2):
        # print "Testing %d" % x
        for base in bases:
            if not is_happy(x, base):
                break
        else:
            return x

def read(f):
    n = int(f.readline())
    for i in xrange(n):
        bases = map(int, f.readline().strip().split())
        yield bases

def main(f, echo_stderr=True):
    import sys
    for i, bases in enumerate(read(f)):
        happiness = solve(bases)
        print "Case #%d: %d" % (i + 1, happiness)
        if echo_stderr:
            print >> sys.stderr, "Case #%d: %d" % (i + 1, happiness)

def test_rebase():
    # print rebase(82, 3)
    # print rebase(5, 3)
    print rebase(91, 9)

def test_is_happy():
    # print is_happy(82, 10)
    # print is_happy(2, 3)
    # print is_happy(5, 3)
    print is_happy(91, 9)
    print is_happy(91, 10)

def test_main():
    from StringIO import StringIO

    input = """
3
2 3
2 3 7
9 10
""".strip()

    output = """
Case #1: 3
Case #2: 143
Case #3: 91
""".strip()

    main(StringIO(input))


if __name__ == '__main__':
    import sys
    # test_rebase()
    # test_is_happy()
    # test_main()
    # sys.exit(0)

    if len(sys.argv) > 1:
        f = open(sys.argv[1])
        main(f)
        f.close()
    else:
        main(sys.stdin)
