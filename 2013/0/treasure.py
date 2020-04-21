#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import defaultdict, namedtuple

Game = namedtuple("Game", "initial_keys nodes")
Node = namedtuple("Node", "number key_to_open keys_in_chest")

def read(f):
    t = int(f.readline().strip())
    for i in xrange(t):
        k, n = map(int, f.readline().strip().split())
        initial_keys = map(int, f.readline().strip().split())
        nodes = []
        for i in xrange(n):
            chest = map(int, f.readline().strip().split())
            key_to_open = chest[0]
            keys_in_chest = chest[2:]
            nodes.append(Node(i+1, key_to_open, keys_in_chest))
        yield Game(initial_keys, nodes)

def find_next_nodes(nodes, keys, exclude=None):
    excluded_node = exclude or []
    next_nodes = []
    for node in nodes:
        if node in excluded_node:
            continue
        if node.key_to_open in keys:
            next_nodes.append(node)
    return next_nodes

def solvable(nodes, keys, node_history):
    available_keys_count = defaultdict(int)
    required_keys_count = defaultdict(int)
    for key in keys:
        available_keys_count[key] += 1
    for node in nodes:
        if node in node_history:
            continue
        for key in node.keys_in_chest:
            available_keys_count[key] += 1
        required_keys_count[node.key_to_open] += 1
    for key in set(available_keys_count.keys() + required_keys_count.keys()):
        if available_keys_count.get(key, 0) < required_keys_count.get(key, 0):
            # IMPOSSIBLE
            return False
    for node in nodes:
        if node in node_history:
            continue
        c = available_keys_count.get(node.key_to_open, 0)
        for key in node.keys_in_chest:
            if key == node.key_to_open:
                c -= 1
        if c > 0:
            continue
        # IMPOSSIBLE
        return False
    return True

def _search(nodes, keys, node_history):
    if not solvable(nodes, keys, node_history):
        return

    path = [node.number for node in node_history]
    # print path

    if len(nodes) == len(node_history):
        yield path
        return

    for node in find_next_nodes(nodes, keys, node_history):
        next_keys = keys[:]
        next_keys.remove(node.key_to_open)
        next_keys += node.keys_in_chest
        for path in search(nodes, next_keys, node_history + [node]):
            yield path

def is_subset(keys1, keys2):
    keys1 = sorted(keys1)
    keys2 = sorted(keys2)
    while keys1 and keys2:
        if keys1 == keys2:
            keys1.pop(0)
            keys2.pop(0)
        elif keys1 > keys2:
            keys2.pop(0)
        else:
            return False
    return not keys1

_cache = {}

def search(nodes, keys, node_history):
    cache_key = frozenset([node.number for node in nodes
                           if node not in node_history])

    for cond in _cache.get(cache_key, []):
        if is_subset(cond, keys):
            continue
        # cut
        return

    count = 0
    for path in _search(nodes, keys, node_history):
        yield path
        count += 1
    if count == 0:
        tmp = []
        for cond in _cache.get(cache_key, []):
            if is_subset(cond, keys):
                continue
            tmp.append(cond)
        if keys:
            tmp.append(keys)
        if tmp:
            _cache[cache_key] = tmp
        elif cache_key in _cache:
            del _cache[cache_key]

def solve(game):
    # print game

    _cache.clear()

    for path in search(game.nodes, game.initial_keys, []):
        return path

    return None

def main(f):
    for i, game in enumerate(read(f)):
        path = solve(game)
        if path:
            result = " ".join(map(str, path))
        else:
            result = "IMPOSSIBLE"
        print "Case #%d: %s" % (i+1, result)

_input = """
3
1 4
1
1 0
1 2 1 3
2 0
3 1 2
3 3
1 1 1
1 0
1 0
1 0
1 1
2
1 1 1
""".strip()

_output = """
Case #1: 2 1 4 3
Case #2: 1 2 3
Case #3: IMPOSSIBLE
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
