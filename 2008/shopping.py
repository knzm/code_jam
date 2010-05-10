import math

def distance(a, b):
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)

def permutations(x):
    if len(x) == 1:
        yield [x[0]]
    elif len(x) >= 2:
        a, b = x[:1], x[1:]
        for p in permutations(b):
            for i in xrange(len(p) + 1):
                yield p[:i] + a + p[i:]

def parse_header(line):
    return map(int, line.strip().split(" "))

def parse_items(line):
    items = []
    for item in line.strip().split(" "):
        if item.endswith("!"):
            item = item[:-1]
            perishable = True
        else:
            perishable = False
        items.append((item, perishable))
    return dict(items)

def parse_shop(line):
    x_pos, y_pos, rest = line.strip().split(" ", 2)
    items = []
    for item in rest.split(" "):
        name, price = item.split(":")
        items.append((name, int(price)))
    return { "location": (int(x_pos), int(y_pos)), "items": dict(items) }

def read_data(f):
    num_items, num_stores, price_of_gas = parse_header(f.readline())
    items = parse_items(f.readline())

    shops = []
    for i in xrange(num_stores):
        shop = parse_shop(f.readline())
        shop["id"] = i + 1
        shops.append((shop["id"], shop))

    return items, dict(shops), price_of_gas

class Solver(object):
    def __init__(self, items, shops, price_of_gas):
        # print "items: ", items
        # print "shops: ", shops
        # print "price_of_gas: ", price_of_gas

        self.items = items
        self.shops = shops
        self.price_of_gas = price_of_gas

        inv = {}
        for item in items:
            inv[item] = [shop_id for shop_id, shop in shops.items()
                                 if item in shop["items"]]
        self.inv = inv

        shop_at = {}
        for shop in shops.values():
            shop_at[shop["location"]] = shop
        self.shop_at = shop_at

        self.distance_cache = {}

    def is_perishable(self, item):
        return self.items[item]

    def get_shop(self, shop_id):
        return self.shops[shop_id]

    # heavy
    def get_distance(self, a, b):
        if a > b: a, b = b, a
        if (a, b) not in self.distance_cache:
            self.distance_cache[(a, b)] = distance(a, b)
        return self.distance_cache[(a, b)]

    def solve(self):
        self.total_cost = float('inf')
        best_plan = None
        for cost, plan in self.rank():
            if cost < self.total_cost:
                self.total_cost = cost
                best_plan = plan
        # print self.total_cost, best_plan
        return self.total_cost

    def rank(self):

        def search(items_to_buy, cart, cost):
            if len(items_to_buy) > 0:
                item = items_to_buy[0]
                for shop_id in self.inv[item]:
                    shop = self.get_shop(shop_id)
                    item_price = shop["items"][item]
                    new_cart = cart + [(shop_id, item)]
                    new_cost = cost + item_price
                    if new_cost > self.total_cost:
                        continue
                    for result in search(items_to_buy[1:], new_cart, new_cost):
                        yield result
            else:
                d = {}
                for shop_id, item in cart:
                    d.setdefault(shop_id, set()).add(item)
                yield cost, d

        for cost, cart in search(self.items.keys(), [], 0):
            if cost > self.total_cost:
                continue
            meter, path = min(self.traverse(cart))

            # plan = self.make_plan(path, cart)
            plan = None

            total_cost = cost + meter * self.price_of_gas
            yield total_cost, plan

    def traverse(self, cart):

        # heavy
        def build_path(history):
            path = [(0, 0)]
            for shop_id, items, perishable in history:
                shop = self.get_shop(shop_id)
                path.append(shop["location"])
                if perishable:
                    path.append((0, 0))
            if path[-1] != (0, 0):
                path.append((0, 0))
            return path

        # heavy
        def calc_meter(path):
            meter = 0
            for a, b in zip(path[:-1], path[1:]):
                meter += self.get_distance(a, b)
            return meter

        def traverse_1(cart):
            cart_items = []
            for shop_id, items in cart.items():
                for item in items:
                    if self.is_perishable(item):
                        perishable = True
                        break
                else:
                    perishable = False
                cart_items.append((shop_id, items, perishable))
            return cart_items

        # heavy
        def traverse_2(cart_iterms):
            for history in permutations(cart_items):
                path = build_path(history)
                meter = calc_meter(path)
                yield meter, path

        cart_items = traverse_1(cart)
        for meter, path in traverse_2(cart_items):
            yield meter, path

    def make_plan(self, path, cart):
        plan = []
        for location in path:
            if location == (0, 0):
                plan.append((None, location, None))
            else:
                shop = self.shop_at[location]
                items = dict([(item, shop["items"][item])
                              for item in cart[shop["id"]]])
                plan.append((shop["id"], location, items))
        return plan

def main(f):
    n = int(f.readline().strip())
    for i in xrange(n):
        # print "Case #%d:" % (i+1)
        solver = Solver(*read_data(f))

        # print "> ",
        # import sys; sys.stdin.readline()

        solver.solve()
        print "Case #%d: %.7f" % (i+1, solver.solve())
        # break
        # print

def test():
    from StringIO import StringIO
    f = StringIO("""\
2
1 2 10
cookies
0 2 cookies:400
4 0 cookies:320
3 3 5
cookies milk! cereal
0 2 cookies:360 cereal:110
4 0 cereal:90 milk:150
-3 -3 milk:200 cookies:200
""")

    f.readline()
    items, shops, price_of_gas = read_data(f)
    # print items
    # print shops
    # print price_of_gas
    solver = Solver(*read_data(f))
    solver.solve()

if __name__ == '__main__':
    # test()
    import sys
    if len(sys.argv) > 1:
        f = open(sys.argv[1])
        main(f)
        f.close()
    else:
        main(sys.stdin)

