def from_alien(number, digits):
    """
    >>> from_alien("9", "0123456789")
    9
    >>> from_alien("13", "0123456789abcdef")
    19
    """
    radix = len(digits)
    dic = dict([(d, i) for i, d in enumerate(digits)])
    result = 0
    for n in number:
        result = result * radix + dic[n]
    return result

def to_alien(number, digits):
    """
    >>> to_alien(9, "oF8")
    'Foo'
    >>> to_alien(19, "01")
    '10011'
    """
    radix = len(digits)
    dic = dict([(i, d) for i, d in enumerate(digits)])
    result = []
    while number > 0:
        result.append(dic[number % radix])
        number /= radix
    return "".join(reversed(result))

def main(f):
    n = int(f.readline().strip())
    for i in xrange(n):
        line = f.readline().strip()
        alien_number, source_language, target_language = line.split()
        neutral_number = from_alien(alien_number, source_language)
        another_number = to_alien(neutral_number, target_language)
        print "Case #%d: %s" % (i + 1, another_number)

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        f = open(sys.argv[1])
        main(f)
        f.close()
    else:
        main(sys.stdin)
