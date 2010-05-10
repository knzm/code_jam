def read(f):
    n = int(f.readline().strip())
    for i in xrange(n):
        yield f.readline().strip()

def print_table(table):
    for row in table:
        print row

def make_table(sentence, welcome):
    table = [None] * len(welcome)
    for row_idx, k in enumerate(welcome):
        table[row_idx] = [0] * len(sentence)
        n = 0
        for col_idx, c in enumerate(sentence):
            if c == k:
                if row_idx == 0:
                    x = 1
                elif col_idx == 0:
                    x = 0
                else:
                    x = table[row_idx - 1][col_idx - 1]
                n += x
            table[row_idx][col_idx] = n
    return table

def search(sentence, welcome):
    table = make_table(sentence, welcome)
    return table[-1][-1]

def main(f):
    welcome = "welcome to code jam"
    for i, sentence in enumerate(read(f)):
        n = search(sentence, welcome)
        print "Case #%d: %04d" % (i + 1, n % 1000)

def test_make_table():
    # welcome = "welcometocodejam"
    welcome = "welcome to code jam"

    # table = make_table("elcomew elcome to code jam", welcome)
    # table = make_table("wweellccoommee to code qps jam", welcome)
    # table = make_table('wwellccomee tto  ccode j jam', welcome)
    # table = make_table("welcome to code jam", welcome)
    table = make_table("wellcomme to ccode  jajmm", welcome)
    print_table(table)

def test_main():
    from StringIO import StringIO

    input = StringIO("""
3
elcomew elcome to code jam
wweellccoommee to code qps jam
welcome to codejam
""".lstrip())

    output = StringIO("""
Case #1: 0001
Case #2: 0256
Case #3: 0000
""".lstrip())

    main(input)

if __name__ == '__main__':
    test = 0
    if test:
        test_make_table()
        # test_main()
    else:
        import sys
        if len(sys.argv) > 1:
            f = open(sys.argv[1])
            main(f)
            f.close()
        else:
            main(sys.stdin)
