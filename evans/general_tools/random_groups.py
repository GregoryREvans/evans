from random import shuffle

items = ["item1", "item2", "item3", "item4", "item5", "item6", "item7", "item8"]
shuffle(items)


def subgroup(list_, n):
    for i in range(0, len(list_), n):
        yield list_[i : i + n]


# groups = list(subgroup(items, 3))
# for group in groups:
#     print(group)

###sample result###
# ['item7', 'item8', 'item3']
# ['item4', 'item1', 'item2']
# ['item6', 'item5']
