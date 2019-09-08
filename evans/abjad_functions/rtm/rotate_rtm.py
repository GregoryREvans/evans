from mtools.rtmrewrite import funnel_tree_to_x


def flatten(lst):
    out = []
    for i in lst:
        if isinstance(i, int):
            out.append(i)
        else:
            out.extend(flatten(i))
    return out


def nested_list_to_rtm(nested_list):
    out_string = ""
    for item in str(nested_list):
        if item == "[":
            out_string += "("
        if item == "]":
            out_string += ")"
        if str.isdigit(item):
            out_string += item
        if item == " ":
            out_string += item
    return out_string


def rotate_tree(rtm_string, n=1):
    opening = rtm_string[:3]
    middle = rtm_string[3:-1]
    closing = rtm_string[-1]
    digits = [_ for _ in middle if str.isdigit(_)]
    digits = (_ for _ in digits[n:] + digits[:n])
    new_middle = ""
    for item in middle:
        if str.isdigit(item):
            new_middle += next(digits)
            continue
        new_middle += item
    return opening + new_middle + closing


def funnel_inner_tree_to_x(rtm_string, x=1):
    opening = rtm_string[:3]
    middle = rtm_string[3:-1]
    closing = rtm_string[-1]
    funnel_list = []
    for _ in funnel_tree_to_x(rtm=middle, x=x):
        funnel_list.append(opening + _ + closing)
    return funnel_list


# rtm = '(1 (3 (2 (1 2 1 1)) 3))'
# for x in funnel_inner_tree_to_x(rtm_string=rtm, x=5):
#     print(x)

# nested_list = [1, 1, [1, [1, 1]], 1]
# rtm = nested_list_to_rtm(nested_list)
# flat = flatten(nested_list)
# rtm = '(1 (2 1 (1 2) 1))'
# rotations = []
# for x in range(len(flatten(nested_list))):
#     new_rtm = rotate_tree(rtm, x)
#     rotations.append(new_rtm)
# # new_rtm = rotate_tree(rtm, 2)
# # print(new_rtm)
# print(rotations)
