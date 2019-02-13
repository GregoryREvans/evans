def cyc(lst):
    count = 0
    while True:
        yield lst[count%len(lst)]
        count += 1
