def print_map(m):
    for row in m:
        print " ".join(map(str, row))

def read(f):
    n = int(f.readline().strip())
    for i in xrange(n):
        height, width = map(int, f.readline().strip().split())
        yield ([map(int, f.readline().strip().split())
                for y in xrange(height)],
               width, height)

def get_neighbors(altitude_map, x, y):
    for nx, ny in [
        (x    , y    ), # Center
        (x    , y - 1), # North
        (x - 1, y    ), # West
        (x + 1, y    ), # East
        (x    , y + 1), # South
        ]:
        if ((0 <= ny < len(altitude_map)) and
            (0 <= nx < len(altitude_map[ny]))):
            nz = altitude_map[ny][nx]
            yield (nx, ny, nz)

def get_source(flow_map, x, y):
    while True:
        sx, sy = flow_map[(x, y)]
        if (sx, sy) == (x, y):
            return (sx, sy)
        x, y = sx, sy

def analyze(altitude_map, width, height):
    from operator import itemgetter
    import string

    flow_map = {}
    for y in xrange(height):
        for x in xrange(width):
            nx, ny, nz = min(get_neighbors(altitude_map, x, y),
                             key=itemgetter(2))
            flow_map[(x, y)] = (nx, ny)

    source_map = {}
    for y in xrange(height):
        for x in xrange(width):
            sx, sy = get_source(flow_map, x, y)
            source_map[(x, y)] = (sx, sy)

    basin_label = {}
    n = 0
    for y in xrange(height):
        for x in xrange(width):
            sx, sy = source_map[(x, y)]
            if (sx, sy) not in basin_label:
                basin_label[(sx, sy)] = string.lowercase[n]
                n += 1

    labeled_map = [None] * height
    for y in xrange(height):
        labeled_map[y] = [None] * width
        for x in xrange(width):
            sx, sy = get_source(flow_map, x, y)
            labeled_map[y][x] = basin_label[(sx, sy)]

    return labeled_map

def main(f):
    for i, (altitude_map, width, height) in enumerate(read(f)):
        print "Case #%d:" % (i + 1)
        # print_map(altitude_map)
        labeled_map = analyze(altitude_map, width, height)
        print_map(labeled_map)

def test_main():
    from StringIO import StringIO

    input = StringIO("""
5
3 3
9 6 3
5 9 6
3 5 9
1 10
0 1 2 3 4 5 6 7 8 7
2 3
7 6 7
7 6 7
5 5
1 2 3 4 5
2 9 3 9 6
3 3 0 8 7
4 9 8 9 8
5 6 7 8 9
2 13
8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8
""".strip())

    output = StringIO("""
Case #1:
a b b
a a b
a a a
Case #2:
a a a a a a a a a b
Case #3:
a a a
b b b
Case #4:
a a a a a
a a b b a
a b b b a
a b b b a
a a a a a
Case #5:
a b c d e f g h i j k l m
n o p q r s t u v w x y z
""".strip())

    main(input)

if __name__ == '__main__':
    test = 0
    if test:
        test_main()
    else:
        import sys
        if len(sys.argv) > 1:
            f = open(sys.argv[1])
            main(f)
            f.close()
        else:
            main(sys.stdin)
