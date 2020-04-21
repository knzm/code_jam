#!/usr/bin/env python
# -*- coding: utf-8 -*-

def read(f):
    n = int(f.readline().strip())
    for i in xrange(n):
        board = [list(f.readline().strip()) for j in xrange(4)]
        yield board
        # skip empty line
        f.readline()

def get_lines(board):
    for row in board:
        yield row
    for col in zip(*board):
        yield col
    yield [board[i][j] for i, j in [(0, 0), (1, 1), (2, 2), (3, 3)]]
    yield [board[i][j] for i, j in [(0, 3), (1, 2), (2, 1), (3, 0)]]

def solve(board):
    for line in get_lines(board):
        tmp = "".join([c for c in line if c != "T"])
        if all([c == "X" for c in tmp]):
            return "X won"
        elif all([c == "O" for c in tmp]):
            return "O won"
    for row in board:
        if "." in row:
            return "Game has not completed"
    return "Draw"

def main(f):
    for i, board in enumerate(read(f)):
        result = solve(board)
        print "Case #%d: %s" % (i+1, result)

_input = """
6
XXXT
....
OO..
....

XOXT
XXOO
OXOX
XXOO

XOX.
OX..
....
....

OOXX
OXXX
OX.T
O..O

XXXO
..O.
.O..
T...

OXXX
XO..
..O.
...O

""".strip()

_output = """
Case #1: X won
Case #2: Draw
Case #3: Game has not completed
Case #4: O won
Case #5: O won
Case #6: O won
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
