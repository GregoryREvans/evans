import re

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    '''
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    (See Toothy's implementation in the comments)
    '''
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]

alist=[
    "voice 1",
    "voice 12",
    "voice 17",
    "voice 2",
    "voice 25",
    "voice 29"]

anotherlist=[
    "1 Flute",
    "2 Violin",
    "3 Bass",]

alist.sort(key=natural_keys)
anotherlist.sort(key=natural_keys)
print(alist)
print(anotherlist)
