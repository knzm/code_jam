import re

def parse(word):
    for m in re.finditer(r'\((.*?)\)|(.)', word):
        if m.group(1):
            yield list(m.group(1))
        else:
            yield [m.group(2)]

def generate(cs, dic, pos=0, prefix=""):
    if not dic:
        return
    if cs:
        for x in cs[0]:
            new_dic = [word for word in dic if word[pos] == x]
            for y in generate(cs[1:], new_dic, pos + 1, prefix + x):
                yield y
    else:
        yield prefix

def main(f):
    L, D, N = map(int, f.readline().strip().split())

    dic = []
    for i in xrange(D):
        dic.append(f.readline().strip())

    for i in xrange(N):
        word = f.readline().strip()
        cs = list(parse(word))

        n = 0
        for text in generate(cs, dic):
            n += 1

        print "Case #%d: %d" % (i + 1, n)
        continue

        # print "%s is parsed as %r" % (word, cs)
        for text in generate(cs, dic):
            print "%s matches %r" % (text, dic)
            # print text
        print

_input = """
3 5 4
abc
bca
dac
dbc
cba
(ab)(bc)(ca)
abc
(abc)(abc)(abc)
(zyx)bc
""".strip()

_output = """
Case #1: 2
Case #2: 1
Case #3: 3
Case #4: 0
""".strip()

def test_main():
    from StringIO import StringIO

    main(StringIO(_input))

def test_generate():
    cs = [['a', 'b'], ['b', 'c'], ['c', 'a']]
    for text in generate(cs):
        print text

if __name__ == '__main__':
    # test_main()
    import sys
    if len(sys.argv) > 1:
        f = open(sys.argv[1])
        main(f)
        f.close()
    else:
        main(sys.stdin)
