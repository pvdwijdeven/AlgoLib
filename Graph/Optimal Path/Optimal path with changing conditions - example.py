from heapq import *
​
​
def dijkstra(matrix, f, t, moves, allowed):
    q, seen = [(0, True, f, ())], set()
    while q:
        (cost, load, v1, path) = heappop(q)
        if (v1, load) not in seen:
            seen.add((v1, load))
            path += (v1,)
            if v1 == t and load:
                return path
            y, x = v1
            for dy, dx in moves:
                v2 = ny, nx = y + dy, x + dx
                if 0 <= ny < len(matrix) and 0 <= nx < len(matrix[ny]):
                    m = matrix[ny][nx]
                    if m in allowed:
                        if dy == dx == 0:
                            if m == 'B':
                                load = not load
                                heappush(q, (cost + 1, load, v2, path))
                        else:
                            heappush(q, (cost + 1 + 1 * load, load, v2, path))
​
​
def checkio(matrix):
    moves = {(-1, 0): 'U', (1, 0): 'D', (0, -1): 'L', (0, 1): 'R', (0, 0): 'B'}
    m = "".join(matrix)
    f = divmod(m.index('S'), len(matrix[0]))
    t = divmod(m.index('E'), len(matrix[0]))
    p = dijkstra(matrix, f, t, moves, '.BSE')
    return "".join([moves[tuple(a - b for a, b in zip(p[i], p[i - 1]))]
                    for i in range(1, len(p))])
​
if __name__ == '__main__':
    #This part is using only for self-checking and not necessary for auto-testing
    ACTIONS = {
        "L": (0, -1),
        "R": (0, 1),
        "U": (-1, 0),
        "D": (1, 0),
        "B": (0, 0)
    }
​
    def check_solution(func, max_time, field):
        max_row, max_col = len(field), len(field[0])
        s_row, s_col = 0, 0
        total_time = 0
        hold_box = True
        route = func(field[:])
        for step in route:
            if step not in ACTIONS:
                print("Unknown action {0}".format(step))
                return False
            if step == "B":
                if hold_box:
                    if field[s_row][s_col] == "B":
                        hold_box = False
                        total_time += 1
                        continue
                    else:
                        print("Stephan broke the cargo")
                        return False
                else:
                    if field[s_row][s_col] == "B":
                        hold_box = True
                    total_time += 1
                    continue
            n_row, n_col = s_row + ACTIONS[step][0], s_col + ACTIONS[step][1],
            total_time += 2 if hold_box else 1
            if 0 > n_row or n_row >= max_row or 0 > n_col or n_row >= max_col:
                print("We've lost Stephan.")
                return False
            if field[n_row][n_col] == "W":
                print("Stephan fell in water.")
                return False
            s_row, s_col = n_row, n_col
            if field[s_row][s_col] == "E" and hold_box:
                if total_time <= max_time:
                    return True
                else:
                    print("You can deliver the cargo faster.")
                    return False
        print("The cargo is not delivered")
        return False
​
    assert check_solution(checkio, 12, ["S...", "....", "B.WB", "..WE"]), "1st Example"
    assert check_solution(checkio, 11, ["S...", "....", "B..B", "..WE"]), "2nd example"