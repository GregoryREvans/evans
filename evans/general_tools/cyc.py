def cyc(lst):
    count = -1
    while True:
        count += 1
        yield lst[count % len(lst)]
