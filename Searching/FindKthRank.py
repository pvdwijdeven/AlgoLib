def rank(my_list, v):
    r = 0
    for l in my_list:
        if l < v:
            r += 1
    return r


def find_rank(my_list, i):
    lt = {}
    eq = {}
    gt = {}
    v = random.choice(my_list.keys())
    for l in my_list.keys():
        if my_list[l] < my_list[v]:
            lt[l] = my_list[l]
        elif my_list[l] == my_list[v]:
            eq[l] = my_list[l]
        elif my_list[l] > my_list[v]:
            gt[l] = my_list[l]
    if len(lt) >= i:
        return find_rank(lt, i)
    elif len(lt) + len(eq) >= i:
        return v
    else:
        return find_rank(gt, i - len(lt) - len(eq))
