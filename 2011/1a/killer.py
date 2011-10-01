#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import defaultdict

def read(f):
    t = int(f.next())
    for i in xrange(t):
        n, m = map(int, f.next().strip().split())
        D = [f.next().strip() for j in xrange(n)]
        L = [f.next().strip() for j in xrange(m)]
        yield D, L

def extract_chars(words):
    chars = set()
    for w in words:
        chars.update(w)
    return chars

def game(letters, words, answer):
    open = {}
    words = list(words)

    tries = []

    miss = 0
    for c in letters:
        if len(words) == 1:
            break

        possible_chars = extract_chars(words)
        if c not in possible_chars:
            continue

        tries.append(c)

        for i in xrange(len(answer)):
            if answer[i] == c:
                open[i] = c

        possible_words = {}
        for w in words:
            possible_words[w] = True
            for i in xrange(len(w)):
                if i in open and w[i] != open[i]:
                    possible_words[w] = False
                    break
                if w[i] == c and i not in open:
                    possible_words[w] = False
                    break
        words = [w for w, v in possible_words.iteritems() if v]

        miss += 1

    # print "[", "".join(tries), "]", answer

    return miss

def solve(d, letters, dic):
    if len(dic) == 1:
        return dic[0]

    score = {}
    max_score = 0
    for n in d:
        if len(d[n]) == 1:
            continue

        for w in d[n]:
            miss = game(letters, d[n], w)
            # print w, miss
            score[w] = miss
            if miss > max_score:
                max_score = miss

    for w in dic:
        if w in score and score[w] == max_score:
            return w
    else:
        assert False

def main(f):
    for i, (dic, lst) in enumerate(read(f)):
        d = defaultdict(list)
        for w in dic:
            d[len(w)].append(w)

        char_at = {}
        for w in dic:
            char_at[w] = defaultdict(list)
            for j, c in enumerate(w):
                char_at[w][c].append(j)

        answers = []
        for j, letters in enumerate(lst):
            # if i == 4 and j == 8:
            #     import pdb; pdb.set_trace()
            # print "letters =", letters
            answer = solve(d, letters, dic)
            answers.append(answer)
            # print
        print "Case #%d: %s" % (i + 1, " ".join(answers))
        # print

_input = """
2
3 2
banana
caravan
pajamas
abcdefghijklmnopqrstuvwxyz
etaoisnhrdlcumwfgypbvkjxqz
4 1
potato
tomato
garlic
pepper
zyxwvutsrqponmlkjihgfedcba
""".strip()

_output = """
Case #1: pajamas caravan
Case #2: garlic
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
