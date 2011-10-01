#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import defaultdict

def read(f):
    t = int(f.next())
    for i in xrange(t):
        n, m = map(int, f.next().strip().split())
        u = map(int, f.next().strip().split())
        v = map(int, f.next().strip().split())
        yield n, zip(u, v)

def build_rooms(n, walls):
    rooms = [range(1, n+1)]
    for p, q in walls:
        # split a room
        for i, room in enumerate(rooms):
            if p in room and q in room:
                j = room.index(p)
                k = room.index(q)
                if j > k:
                    j, k = k, j
                rooms.pop(i)
                rooms.append(room[j:k+1])
                rooms.append(room[:j+1] + room[k:])
                break
    return rooms

def check(rooms, state):
    used_colors = set(state.values())

    for room in rooms:
        colors = set()
        for p in room:
            c = state.get(p)
            if c is not None:
                colors.add(c)
        for c in used_colors:
            if c not in colors:
                return False

    return True

def solve(pt, rooms, walls, used_colors):
    v = defaultdict(int)
    for p, q in walls:
        v[p] += 1
        v[q] += 1
    pt = sorted(pt, key=v.__getitem__, reverse=True)

    queue = [{pt[0]: 1}]
    while queue:
        state = queue.pop(0)
        if not check(rooms, state):
            continue
        for v in pt:
            if v not in state:
                break
        else:
            # import pdb; pdb.set_trace()
            n = len(set(state.values()))
            if n == used_colors:
                yield n, state

        colors = sorted(set(state.values()))
        new_state = state.copy()
        new_state[v] = colors[-1] + 1
        queue.append(new_state)
        for c in colors:
            new_state = state.copy()
            new_state[v] = c
            queue.append(new_state)

def main(f):
    for i, (n, walls) in enumerate(read(f)):
        # print n, walls
        rooms = build_rooms(n, walls)
        pt = range(1, n+1)
        min_space = min(map(len, rooms))
        for used_colors, state in solve(pt, rooms, walls, min_space):
            print used_colors, state
            # break

_input = """
2
4 1
2
4
8 3
1 1 4
3 7 7
""".strip()

_output = """
Case #1: 3
1 2 1 3
Case #2: 3
1 2 3 1 1 3 2 3
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
    test = True
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
