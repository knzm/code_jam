#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import defaultdict

def read(f):
    t = int(f.next())
    for i in xrange(t):
        n = int(f.next().strip())
        arr = map(int, f.next().strip().split())
        assert len(arr) == n
        yield arr

def make_graph(arr):
    g = {}
    for i, n in enumerate(arr):
        g[i+1] = n
    return g

def split_components(g):
    components = []
    visited = set()
    for node in g:
        component = []
        while node not in visited:
            visited.add(node)
            component.append(node)
            node = g[node]
        if component:
            components.append(sorted(component))
    return components

def permutations(L):
    if len(L) == 1:
        yield [L[0]]
    elif len(L) >= 2:
        a, b = L[0:1], L[1:]
        for p in permutations(b):
            for i in range(len(p)+1):
                yield p[:i] + a + p[i:]

_trans = {
    2: {0: 1, 2: 1},
    3: {0: 2, 1: 3, 3: 1},
    4: {0: 9, 1: 8, 2: 6, 4: 1},
    5: {0: 44, 1: 45, 2: 20, 3: 10, 5: 1},
    6: {0: 265, 1: 264, 2: 135, 3: 40, 4: 15, 6: 1},
    7: {0: 1854, 1: 1855, 2: 924, 3: 315, 4: 70, 5: 21, 7: 1},
    8: {0: 14833, 1: 14832, 2: 7420, 3: 2464, 4: 630, 5: 112, 6: 28, 8: 1},
    9: {0: 133496, 1: 133497, 2: 66744, 3: 22260, 4: 5544, 5: 1134, 6: 168, 7: 36, 9: 1},
    10: {0: 1334961, 1: 1334960, 2: 667485, 3: 222480, 4: 55650, 5: 11088, 6: 1890, 7: 240, 8: 45, 10: 1},
}

def trans(n, normalize=True):
    if n in _trans:
        d = _trans[n]
    else:
        d = defaultdict(int)
        for seq in permutations(range(n)):
            match = 0
            for i, x in enumerate(seq):
                if i == x:
                    match += 1
            d[match] += 1
        _trans[n] = dict(d)
    if normalize:
        if d:
            num = sum(d.values())
            return [float(d.get(i, 0)) / num for i in xrange(max(d.keys())+1)]
        else:
            return []
    else:
        return dict(d)

_expected_length = {
    2: 2.0,
    3: 4.5,
    4: 5.86666666667,
    5: 7.64832535885,
    6: 9.35688859304,
    7: 11.0766013325,
    8: 12.7946841741,
    9: 14.5129864125,
    10: 16.231266594,
}

def expected_length(key):
    if key in _expected_length:
        return _expected_length[key]
    t = trans(key)
    n = 1.0 / t[0]
    for j, p in enumerate(reversed(t[1:])):
        if j > 0 and p > 0:
            n += p / (1 - t[0]) * expected_length(j)
    _expected_length[key] = n
    return n

def main(f):
    for i, arr in enumerate(read(f)):
        g = make_graph(arr)
        gs = split_components(g)
        unordered = defaultdict(int)
        for x in map(len, gs):
            if x != 1:
                unordered[x] += 1.0
        # print arr, gs
        # print dict(unordered)
        n = 0.0
        for key, count in unordered.iteritems():
            n += expected_length(key) * count
        print "Case #%d: %.6f" % (i + 1, n)

_input = """
3
2
2 1
3
1 3 2
4
2 1 4 3
""".strip()

_output = """
Case #1: 2.000000
Case #2: 2.000000
Case #3: 4.000000
""".strip()

def test_main(compare=False):
    import sys
    from difflib import unified_diff
    from StringIO import StringIO

    if compare:
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

    else:
        main(StringIO(_input))

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
