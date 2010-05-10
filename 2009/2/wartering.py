import math
import random

def read(f):
    c = int(f.readline())
    for i in xrange(c):
        n = int(f.readline())
        yield [map(int, f.readline().strip().split()) for j in xrange(n)]

def vec_prod(v1, v2):
    return v1[0] * v2[0] + v1[1] * v2[1]

def norm2(v):
    return vec_prod(v, v)

def norm(v):
    return math.sqrt(norm2(v))

def distance(x1, y1, x2, y2):
    return norm((x1 - x2, y1 - y2))

def vec_normalize(v):
    nv = norm(v)
    return v[0] / nv, v[1] / nv

def get_outer_circle2(p1, p2):
    x1, y1, r1 = p1
    x2, y2, r2 = p2

    x = float(x1 + x2) / 2.0
    y = float(y1 + y2) / 2.0
    r = distance(x1, y1, x2, y2) / 2.0

    vx = float(x1 - x2) / 2.0
    vy = float(y1 - y2) / 2.0
    dx = vx * (r1 - r2) / 2.0
    dy = vy * (r1 - r2) / 2.0
    dr = (r1 + r2) / 2.0

    return x + dx, y + dy, r + dr

def get_outer_circle3(p1, p2, p3):
    x1, y1, r1 = p1
    x2, y2, r2 = p2
    x3, y3, r3 = p2

    v1 = (x1 - x3, y1 - y3)
    v2 = (x2 - x3, y2 - y3)

    nv11 = float(norm2(v1))
    nv22 = float(norm2(v2))
    if nv11 == 0 or nv22 == 0:
        raise ValueError

    nv12 = float(vec_prod(v1, v2))

    if nv11 * nv22 == nv12 * nv12:
        raise ValueError

    c1 = 1 - nv12 * (nv22 - nv12) / (nv11 * nv22 - nv12 * nv12)
    c2 = 1 - nv12 * (nv11 - nv12) / (nv11 * nv22 - nv12 * nv12)

    x = (c1 * v1[0] + c2 * v2[0]) / 2.0
    y = (c1 * v1[1] + c2 * v2[1]) / 2.0
    r = norm((x, y))

    return x + x3, y + y3, r

def all_contained(gx, gy, gr, m):
    for x, y, r in m:
        if distance(gx, gy, x, y) > gr:
            return False
    else:
        return True

def extend(gx, gy, gr, m):
    for x, y, r in m:
        d = distance(gx, gy, x, y)
        if d + r > gr:
            dr = d + r - gr
            dx, dy = vec_normalize((x - gx, y - gy))
            gx += dx * dr / 2
            gy += dy * dr / 2
            gr += dr / 2
    return gx, gy, gr

def get_outer_circle(m):
    n = len(m)

    for i in xrange(n):
        for j in xrange(i + 1, n):
            # consists of 2 points
            gx, gy, gr = get_outer_circle2(m[i], m[j])
            outers = []
            for k, (x, y, r) in enumerate(m):
                if distance(gx, gy, x, y) > gr:
                    outers.append(k)
            if not outers:
                yield extend(gx, gy, gr, m)
            # consists of 3 points
            for k in outers:
                try:
                    gx, gy, gr = get_outer_circle3(m[i], m[j], m[k])
                    if all_contained(gx, gy, gr, m):
                        yield extend(gx, gy, gr, m)
                except ValueError:
                    pass

def solve_sub(m):
    from operator import itemgetter
    if len(m) == 0:
        raise ValueError
    elif len(m) == 1:
        return m[0]
    answers = list(get_outer_circle(m))
    if answers:
        x, y, r = sorted(answers, key=itemgetter(2))[0]
        # print m
        # print x, y, r
        return x, y, r
    else:
        raise ValueError

def iter_bits(nbits):
    end = (1 << nbits) - 1
    for n in xrange(1, end - 1):
        yield [(n >> i) & 1 for i in xrange(nbits)]

def solve_simple(m):
    if len(m) == 1:
        return m[0][2]
    a = []
    for bits in iter_bits(len(m)):
        m1 = []
        m2 = []
        for i, b in enumerate(bits):
            if b:
                m1.append(m[i])
            else:
                m2.append(m[i])
        # print n, bits[::-1],
        try:
            x1, y1, r1 = solve_sub(m1)
            x2, y2, r2 = solve_sub(m2)
            a.append(max(r1, r2))
            # print (r1, r2)
        except ValueError:
            # print
            pass
    # if not a:
    #     import pdb; pdb.set_trace()
    return min(a)

class FastSolver(object):
    def __init__(self, m):
        self.m = m

    def search(self, area1, area2):
        if tuple(area1) in self.seen:
            return
        self.seen[tuple(area1)] = True
        try:
            x1, y1, r1 = solve_sub([self.m[i] for i in area1])
            x2, y2, r2 = solve_sub([self.m[i] for i in area2])
            r = max(r1, r2)
            print sorted(area1), r
        except ValueError:
            pass
        else:
            if self.min_r is None or r <= self.min_r:
                self.min_r = r
                for j in area2:
                    self.search(area1.union([j]), area2.difference([j]))

    def solve(self):
        self.min_r = None
        self.seen = {}
        area1 = set([0])
        area2 = set(xrange(1, len(self.m)))
        self.search(area1, area2)
        return self.min_r

def solve_fast(m):
    if len(m) == 1:
        return m[0][2]

    # d = {}
    # for i in xrange(len(m)):
    #     for j in xrange(i + 1, len(m)):
    #         x1, y1, r1 = m[i]
    #         x2, y2, r2 = m[j]
    #         d[(i, j)] = d[(j, i)] = distance(x1, y1, x2, y2)

    solver = FastSolver(m)
    min_r = solver.solve()
    return min_r

def generate(pool, evals, elite_num, elite_copy=3):
    pool_size = len(pool)
    new_pool = []

    # elite preservation
    elites = []
    pairs = [(ev, gene) for ev, gene in zip(evals, pool) if ev is not None]
    for ev, gene in sorted(pairs, reverse=True)[:elite_num]:
        elites.append(gene)
    for i in xrange(elite_copy):
        new_pool.extend(elites[:])

    # roulette selection
    total_eval = 0
    for ev in evals:
        if ev is not None:
            total_eval += ev
    cum_probs = []
    cum_prob = 0
    for ev in evals:
        if ev is not None:
            cum_prob += ev / total_eval
        cum_probs.append(cum_prob)
    while len(new_pool) < pool_size:
        p = random.random()
        for i, cum_prob in enumerate(cum_probs):
            if p < cum_prob:
                new_pool.append(pool[i][:])
                break

    return new_pool

def crossover(gene1, gene2):
    for i, (b1, b2) in enumerate(zip(gene1, gene2)):
        if random.random() < 0.5:
            gene1[i] = b2
            gene2[i] = b1

def solve_ga(m):
    if len(m) == 1:
        return m[0][2]

    pool_size = 100

    pool = []
    for i in xrange(pool_size):
        gene = [random.randint(0, 1) for i in xrange(len(m))]
        pool.append(gene)

    result = {}
    convergent = 0
    ngen = 0
    last_elites = None
    while True:
        ngen += 1
        evals = []
        for i, bits in enumerate(pool):
            m1 = []
            m2 = []
            if tuple(bits) in result:
                r = result[tuple(bits)]
            else:
                for j, b in enumerate(bits):
                    if b:
                        m1.append(m[j])
                    else:
                        m2.append(m[j])
                try:
                    x1, y1, r1 = solve_sub(m1)
                    x2, y2, r2 = solve_sub(m2)
                    r = max(r1, r2)
                    result[tuple(bits)] = r
                except ValueError:
                    r = None
            if r:
                evals.append(1 / (r ** 2))
            else:
                evals.append(None)

        pool = generate(pool, evals, 5)
        elites = pool[:5]
        print ngen, result[tuple(pool[0])]
        if ngen > 100 and elites == last_elites:
            convergent += 1
        else:
            convergent = 0
        if convergent > 10:
            break
        last_elites = [gene[:] for gene in elites]

        for i in xrange(5, pool_size):
            for j in xrange(i, pool_size):
                if random.random() < 0.2:
                    crossover(pool[i], pool[j])
    return result[tuple(last_elites[0])]

solve = solve_fast

def test_solve():
    print solve([[20, 10, 2], [20, 20, 2], [40, 10, 3]])

def main(f):
    for i, m in enumerate(read(f)):
        r = solve(m)
        print "Case #%d: %f" % (i + 1, r)

def test_main():
    from StringIO import StringIO

    input = """
5
3
20 10 2
20 20 2
40 10 3
3
20 10 3
30 10 3
40 10 3
5
100 100 1
140 100 1
100 130 1
100 500 1
150 500 1
8
100 100 1
110 100 1
100 110 1
110 110 1
200 200 1
210 200 1
200 210 1
210 210 1
4
100 100 1
200 100 1
200 103 1
300 103 1
""".strip()

    output = """
Case #1: 7.000000
Case #2: 8.000000
Case #3: 26.000000
Case #4: 8.071067
Case #5: 51
""".strip()

    main(StringIO(input))

if __name__ == '__main__':
    import sys
    # test_solve()
    # test_main()
    # sys.exit(0)

    if len(sys.argv) > 1:
        f = open(sys.argv[1])
        main(f)
        f.close()
    else:
        main(sys.stdin)
