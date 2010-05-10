import re

def make_board(lines):
    return [list(line) for line in lines]

def read(f):
    n = int(f.readline().strip())
    for i in xrange(n):
        w, q = map(int, f.readline().strip().split())
        board = make_board([f.readline().strip() for j in xrange(w)])
        queries = map(int, f.readline().strip().split())
        yield board, queries

def search(board, queue):
    while True:
        x, y, expression = queue.pop(0)
        # import pdb; pdb.set_trace()
        expression = expression + [board[y][x]]
        if len(expression) % 2 == 1:
            yield "".join(expression)
        for nx, ny in [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]:
            if 0 <= nx < len(board) and 0 <= ny < len(board):
                queue.append((nx, ny, expression))

def eval_expression(expression):
    try:
        return eval(expression)
    except SyntaxError:
        print expression
        raise

def solve(query, board):
    queue = [(x, y, []) for x in xrange(len(board)) for y in xrange(len(board))
                        if re.match(r'^\d+$', board[y][x])]
    for expression in search(board, queue):
        if eval_expression(expression) == query:
            return expression

def main(f):
    for i, (board, queries) in enumerate(read(f)):
        print "Case #%d:" % (i + 1)
        for query in queries:
            print solve(query, board)

def test_main():
    from StringIO import StringIO

    input = """
2
5 3
2+1-2
+3-4+
5+2+1
-4-0-
9+5+1
20 30 40
3 2
2+1
+4+
5+1
2 20
""".strip()

    output = """
Case #1:
1+5+5+9
3+4+5+9+9
4+9+9+9+9
Case #2:
2
5+5+5+5
""".strip()

    main(StringIO(input))


if __name__ == '__main__':
    import sys
    # test_main()
    # sys.exit(0)

    if len(sys.argv) > 1:
        f = open(sys.argv[1])
        main(f)
        f.close()
    else:
        main(sys.stdin)
