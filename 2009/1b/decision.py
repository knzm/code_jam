from sexpParser import sexp

def parse_sexp(s):
    return sexp.parseString(s).asList()[0]

def read(f):
    n = int(f.readline())
    for i in xrange(n):
        n_lines = int(f.readline().strip())
        buffer = "".join([f.readline() for j in xrange(n_lines)])
        tree = parse_sexp(buffer)
        n_animals = int(f.readline().strip())
        animals = []
        for j in xrange(n_animals):
            cols = f.readline().strip().split()
            animals.append((cols[0], cols[2:]))
        yield tree, animals

def walk_tree(animal, tree, r=1.0):
    node = tree
    weight = node[0]
    if len(node) > 1:
        r *= float(weight)
        feature = node[1]
        if feature in animal[1]:
            return walk_tree(animal, node[2], r)
        else:
            return walk_tree(animal, node[3], r)
    else:
        r *= float(weight)
        return r

def main(f):
    for i, (tree, animals) in enumerate(read(f)):
        print "Case #%d:" % (i + 1)
        for animal in animals:
            print "%.7f" % walk_tree(animal, tree)

def test_main():
    from StringIO import StringIO

    input = """
2
3
(0.5 cool
  ( 1.000)
  (0.5 ))
2
anteater 1 cool
cockroach 0
13
(0.2 furry
  (0.81 fast
    (0.3)
    (0.2)
  )
  (0.1 fishy
    (0.3 freshwater
      (0.01)
      (0.01)
    )
    (0.1)
  )
)
3
beaver 2 furry freshwater
trout 4 fast freshwater fishy rainbowy
dodo 1 extinct
""".strip()

    output = """
Case #1:
0.5000000
0.2500000
Case #2:
0.0324000
0.0000600
0.0020000
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
