def read(f):
    n = int(f.readline())
    for i in xrange(n):
        rows = int(f.readline())
        yield [map(int, f.readline().strip()) for j in xrange(rows)]

def best_position(row):
    for i in reversed(xrange(0, len(row))):
        if row[i]:
            return i
    else:
        return 0

def test_best_position():
    assert best_position([1, 0], 0) == 0

def swap(a, i, j):
    a[i], a[j] = a[j], a[i]

def get_first_unordered(pos):
    for i in xrange(len(pos)):
        if pos[i] > i:
            return i
    else:
        return -1

def solve(m):
    rank = len(m)
    n = 0
    pos = [best_position(row) for row in m]
    while True:
        first_unordered = get_first_unordered(pos)
        if first_unordered < 0:
            break

        swapped = False
        for i in xrange(first_unordered, rank):
            if pos[i] <= first_unordered:
                for j in xrange(i, first_unordered, -1):
                    swap(m,   j-1, j)
                    swap(pos, j-1, j)
                    n += 1
                    swapped = True
                break
        if not swapped:
            import pdb; pdb.set_trace()
    return n

def test_solve():
    m = [[1, 1, 1, 0],
         [1, 1, 0, 0],
         [1, 1, 0, 0],
         [1, 0, 0, 0]]
    print solve(m)

def main(f):
    for i, m in enumerate(read(f)):
        n = solve(m)
        print "Case #%d: %d" % (i + 1, n)

def test_main():
    from StringIO import StringIO

    input = """
3
2
10
11
3
001
100
010
4
1110
1100
1100
1000
""".strip()

    output = """
Case #1: 0
Case #2: 2
Case #3: 4
""".strip()

    main(StringIO(input))

if __name__ == '__main__':
    import sys
    # test_solve()
    # test_main()
    # sys.exit(0)

    if len(sys.argv) > 1:
        f = open(sys.argv[1])
        main(f)
        f.close()
    else:
        main(sys.stdin)
