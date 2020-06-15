def normalize_sum(integer_list, desired_sum=1):
    sum = 0
    for _ in integer_list:
        sum = sum + _ / desired_sum
    normalized_list = []
    for _ in integer_list:
        normalized_list.append(_ / sum)
    return normalized_list


# ##DEMO###
# weights = [15, 6, 14, 4, 16, 6, 14, 4, 16, 5]
# print(normalize_sum(integer_list=weights, desired_sum=1))
#
# print("checking")
# checker = 0
# for _ in normalize_sum(integer_list=weights):
#     checker = checker + _
# print(checker)
