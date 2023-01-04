def choose_obj(choose_list, obj_list, q, f=False):
    for i in choose_list:
        print(i)
    ans = int(input(q))
    if f and ans == 0:
        return ""
    return obj_list[ans - 1]


# def choose_int(choose_list, q):
#     for i in choose_list:
#         print(i)
#     ans = int(input(q))
#     return ans
