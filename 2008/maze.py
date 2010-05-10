SOUTH = 0 #  1,  0
WEST  = 1 #  0,  1
NORTH = 2 # -1,  0
EAST  = 3 #  0, -1

direction_label = "SWNE"

def left_of(direction):
    return (direction + 3) % 4

def right_of(direction):
    return (direction + 1) % 4

def back_of(direction):
    return (direction + 2) % 4

def vector_from_direction(direction):
    if direction % 2:
        # EAST(3) or WEST(1)
        return (direction - 2, 0)
    else:
        # NORTH(2) or SOUTH(0)
        return (0, direction - 1)

def walk(path, position, direction):
    last_position = position
    last_direction = direction
    turn = []
    for a in path:
        if a == 'L':
            # Turn left
            direction = left_of(direction)
            turn.append(a)
        elif a == 'R':
            # Turn right
            direction = right_of(direction)
            turn.append(a)
        elif a == 'W':
            # Walk through
            yield (last_position, last_direction, "".join(turn) + "W")
            v = vector_from_direction(direction)
            x = position[0] + v[0]
            y = position[1] + v[1]
            position = (x, y)
            last_position = position
            last_direction = direction
            turn = []
        else:
            raise ValueError, a
    yield (last_position, last_direction, "".join(turn))

def log(space, position, direction, is_open):
    if direction in space and space[direction] != is_open:
        print ("At %r direction %s was once %s then %s"
               % (position, direction_label[direction], space[direction], is_open))
        assert False
    # print ("At %r, direction %s is set to %s"
    #        % (position, direction_label[direction], is_open))
    space[direction] = is_open

def solve(path, spaces=None, position=None, direction=None):
    if spaces is None:
        spaces = {}
    if position is None:
        position = (0, 0)
    if direction is None:
        direction = SOUTH

    trace = list(walk(path, position, direction))

    for position, direction, motion in trace[1:-1]:
        # print position, direction, motion
        space = spaces.setdefault(position, {})
        if motion == 'LW':
            # Can walk to the left
            log(space, position, left_of(direction), True)
        elif motion == 'W':
            # Can't walk to the left
            log(space, position, left_of(direction), False)
            # Can walk through
            log(space, position, direction, True)
        elif motion == 'RW':
            # Can't walk to the left
            log(space, position, left_of(direction), False)
            # Can't walk through
            log(space, position, direction, False)
            # Can walk to the right
            log(space, position, right_of(direction), True)
        elif motion == 'RRW':
            # Can't walk to the left
            log(space, position, left_of(direction), False)
            # Can't walk through
            log(space, position, direction, False)
            # Can't walk to the right
            log(space, position, right_of(direction), False)
            # Can walk back
            log(space, position, back_of(direction), True)
        else:
            raise ValueError, trace

    position, direction, motion = trace[-1]

    return spaces, position, direction

def get_bounding_box(points):
    xs = set()
    ys = set()
    for x, y in points:
        xs.add(x)
        ys.add(y)

    min_x = min(xs); max_x = max(xs)
    min_y = min(ys); max_y = max(ys)
    return (min_x, min_y, max_x, max_y)

def get_character(d):
    val = 0
    if d[NORTH]: val |= 1
    if d[SOUTH]: val |= 2
    if d[WEST ]: val |= 4
    if d[EAST ]: val |= 8
    return "%x" % val

def main(f):
    n = int(f.readline().strip())
    for i in xrange(n):
        line = f.readline().strip()
        forward, backward = line.split()

        print "Case #%d:" % (i + 1)
        spaces, position, direction = solve(forward)
        direction = back_of(direction)
        spaces, position, direction = solve(backward, spaces, position, direction)
        (min_x, min_y, max_x, max_y) = get_bounding_box(spaces.keys())
        for y in xrange(max_y, min_y-1, -1):
            print "".join([get_character(spaces[(x, y)])
                           for x in xrange(min_x, max_x+1)])

def test():
    spaces, position, direction = solve("WRWWLWWLWWLWLWRRWRWWWRWWRWLW")
    print ("last position and direction: %r, %s"
           % (position, direction_label[direction]))
    direction = back_of(direction)
    spaces, position, direction = solve("WWRRWLWLWWLWWLWWRWWRWWLW",
                                          spaces, position, direction)

    xs = set()
    ys = set()
    for x, y in spaces.keys():
        xs.add(x)
        ys.add(y)

    min_x = min(xs); max_x = max(xs)
    min_y = min(ys); max_y = max(ys)

    for y in xrange(max_y, min_y-1, -1):
        for x in xrange(min_x, max_x+1):
            info = spaces.get((x, y))
            val = 0
            if info[NORTH]: val |= 1
            if info[SOUTH]: val |= 2
            if info[WEST ]: val |= 4
            if info[EAST ]: val |= 8
            print "%x" % val,
            # print (x, y), info
        print


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        f = open(sys.argv[1])
        main(f)
        f.close()
    else:
        main(sys.stdin)
