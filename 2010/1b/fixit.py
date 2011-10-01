#!/usr/bin/env python

def read(f):
    t = int(f.readline())
    for i in xrange(t):
        cur_path = []
        new_path = []
        n, m = map(int, f.readline().strip().split())
        for j in xrange(n):
            cur_path.append(f.readline().strip())
        for j in xrange(m):
            new_path.append(f.readline().strip())
        yield cur_path, new_path

def main(f):
    for i, (cur_path, new_path) in enumerate(read(f)):
        count = 0
        tree = {}
        for path in cur_path:
            d = tree
            for p in path.strip('/').split('/'):
                d = d.setdefault(p, {})
        for path in new_path:
            d = tree
            for p in path.strip('/').split('/'):
                if p not in d:
                    count += 1
                    d[p] = {}
                d = d[p]
        print "Case #%d: %d" % (i + 1, count)


_input = """
3
0 2
/home/gcj/finals
/home/gcj/quals
2 1
/chicken
/chicken/egg
/chicken
1 3
/a
/a/b
/a/c
/b/b
""".strip()

_output = """
Case #1: 4
Case #2: 0
Case #3: 4
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
