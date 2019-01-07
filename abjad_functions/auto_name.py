a = [1, 2, 3, 4]
b = [2, 3, 4, 5]
c = [3, 4, 5, 6]
d = [10, 11, 12]

lst_dict = {
    'List ' + str(i + 1): sub_lst
    for i, sub_lst in enumerate([a, b, c, d])
}
'''
    print(lst_dict)
    >>> {'List 1': [1, 2, 3, 4], 'List 2': [2, 3, 4, 5], 'List 3': [3, 4, 5, 6], 'List 4': [10, 11, 12]}
'''