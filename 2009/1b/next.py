def read(f):
    n = int(f.readline())
    for i in xrange(n):
        yield int(f.readline())

def get_next_digit(n, digits):
    for digit in digits:
        if digit > n:
            return digit
    else:
        return None

def get_sorted_digits(n_digits):
    return [digit for digit in sorted(n_digits) if digit != "0"]

def next_number(n):
    n_digits = list(str(n))

    for suffix_len in xrange(len(n_digits)):
        pos = len(n_digits) - suffix_len - 1
        prefix = n_digits[:pos]
        suffix = n_digits[pos+1:]
        n = get_next_digit(n_digits[pos], get_sorted_digits(suffix))
        if n:
            rest = n_digits[pos:]
            rest.remove(n)
            next_suffix = get_sorted_digits(rest)[-suffix_len:]
            if len(next_suffix) < suffix_len:
                next_suffix = ["0"] * (suffix_len - len(next_suffix)) + next_suffix
                
            # print prefix, n, next_suffix
            return "".join(prefix + [n] + next_suffix)
    digits = get_sorted_digits(n_digits)
    padding = ["0"] * (len(n_digits) - len(digits) + 1)
    return "".join(digits[:1] + padding + digits[1:])

def main(f):
    for i, n in enumerate(read(f)):
        x = next_number(n)
        print "Case #%d: %s" % (i + 1, x)

def test_next_number():
    # print next_number(115)
    # print next_number(1051)
    # print next_number(6233)
    # print next_number(151)
    # print next_number(511)
    print next_number(840)

def test_main():
    from StringIO import StringIO

    input = """
3
115
1051
6233
""".strip()

    output = """
Case #1: 151
Case #2: 1105
Case #3: 6323
""".strip()

    main(StringIO(input))


if __name__ == '__main__':
    import sys
    # test_next_number()
    # test_main()
    # sys.exit(0)

    if len(sys.argv) > 1:
        f = open(sys.argv[1])
        main(f)
        f.close()
    else:
        main(sys.stdin)
