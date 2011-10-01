#!/usr/bin/env python
# -*- coding: utf-8 -*-

def read(f):
    t = int(f.next())
    for i in xrange(t):
        p, w = map(int, f.next().strip().split())
        m = [set() for j in xrange(p)]
        for pair in f.next().strip().split():
            x1, x2 = map(int, pair.split(","))
            m[x1].add(x2)
            m[x2].add(x1)
        yield m

def dijkstra(nodes, edges, start):
    import sys
    from copy import deepcopy

    dist = [sys.maxint for v in nodes]
    prev = [None for v in nodes]

    dist[start] = 0
    Q = set(nodes)

    while len(Q) > 0:
        u = min(Q, key=dist.__getitem__)
        Q.remove(u)
        for v in edges[u]:
            alt = dist[u] + 1
            if alt < dist[v]:
                dist[v] = alt
                prev[v] = u

    return dist, prev

def search(m):
    nodes = range(len(m))
    dist, prev = dijkstra(nodes, m, 0)
    # print dist[1] - 1, prev

    seen = set()
    q = [(frozenset([0]), frozenset())]
    while q:
        own, threaten = q.pop(0)
        if len(own) > dist[1]:
            continue
        # print own, threaten
        for node in own:
            adj = m[node] - own
            new_threaten = threaten.union(adj)
            for target in adj:
                if dist[target] < len(own):
                    continue
                if target == 1:
                    yield own, new_threaten
                    continue
                new_own = own.union([target])
                if new_own in seen:
                    continue
                q.append((new_own, new_threaten))
                seen.add(frozenset(new_own))

def _evaluate(m, path):
    own = set([path[0]])
    threaten = set()
    for node in path[:-1]:
        own.add(node)
        for node2 in m[node]:
            if node2 not in own:
                threaten.add(node2)
    return len(threaten - own)

def main(f):
    for i, m in enumerate(read(f)):
        # print "Case #%d" % (i + 1)
        # print m
        answer = None
        for own, threaten in search(m):
            print own # , threaten - own
            continue
            c = len(own) - 1
            t = len(threaten - own)
            # print c, t
            if answer is None or answer[1] < t:
                answer = (c, t)
            # score = evaluate(m, path)
            # answers.append((path, score))
        # path, score = max(answers, key=lambda kv: kv[1])
        # print "Case #%d: %d %d" % (i + 1, c, t)

_input = """
4
2 1
0,1
3 3
0,1 1,2 0,2
5 5
0,4 0,2 2,4 1,2 1,4
7 9
0,6 0,2 0,4 2,4 3,4 2,3 3,5 4,5 1,5
""".strip()

_output = """
Case #1: 0 1
Case #2: 0 2
Case #3: 1 2
Case #4: 2 4
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
    compare = False
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
