import abjad


meters = [
    abjad.Meter(pair)
    for pair in [
        (5, 4),
        (9, 8),
        (4, 4),
        (7, 8),
        (3, 4),
        (5, 8),
        (2, 4),
        (3, 8),
        (5, 16),
        (1, 4),
        (3, 16),
        (1, 8),
    ]
]

for meter in meters:
    print(meter)
    inventories = [x for x in enumerate(meter.depthwise_offset_inventory)]
    if meter.denominator == 4:
        print(inventories[-1][0])
        print(inventories[-1][1])
        print("")
    else:
        print(inventories[-2][0])
        print(inventories[-2][1])
        print("")
