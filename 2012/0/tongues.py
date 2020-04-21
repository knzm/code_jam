#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import string

def read(f):
    n = int(f.readline())
    for i in xrange(n):
        yield f.readline().strip("\n")

def make_mapping():
    letters = string.ascii_lowercase + ' '
    mapping = dict([(c, None) for c in letters])
    mapping.update({'a': 'y', 'o': 'e', 'z': 'q'})
    src = ("ejp mysljylc kd kxveddknmc re jsicpdrysi"
           "rbcpc ypc rtcsra dkh wyfrepkym veddknkmkrkcd"
           "de kr kd eoya kw aej tysr re ujdr lkgc jv")
    dst = ("our language is impossible to understand"
           "there are twenty six factorial possibilities"
           "so it is okay if you want to just give up")
    mapping.update(zip(src, dst))
    unused_in_googlerese = set(letters)
    unused_in_english = set(letters)
    for k, v in sorted(mapping.iteritems()):
        if v is None:
            continue
        unused_in_googlerese.remove(k)
        unused_in_english.remove(v)
    if len(unused_in_googlerese) == 0 and len(unused_in_english) == 0:
        pass
    elif len(unused_in_googlerese) == 1 and len(unused_in_english) == 1:
        k = list(unused_in_googlerese)[0]
        v = list(unused_in_english)[0]
        mapping[k] = v
    else:
        assert False

    return mapping

def solve(line, mapping):
    return re.sub(r'[a-z ]', lambda m: mapping[m.group(0)], line)

def main(f):
    mapping = make_mapping()
    for i, line in enumerate(read(f)):
        decoded = solve(line, mapping)
        print "Case #%d: %s" % (i+1, decoded)

_input = """
3
ejp mysljylc kd kxveddknmc re jsicpdrysi
rbcpc ypc rtcsra dkh wyfrepkym veddknkmkrkcd
de kr kd eoya kw aej tysr re ujdr lkgc jv
""".strip()

_output = """
Case #1: our language is impossible to understand
Case #2: there are twenty six factorial possibilities
Case #3: so it is okay if you want to just give up
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
