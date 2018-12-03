def unique(a):
    return list(set(a))

def intersect(a, b):
    return list(set(a) & set(b))

def union(a, b):
    return list(set(a) | set(b))

if __name__ == "__main__":
    a = [0,1,2,0,1,2,3,4,5,6,7,8,9]
    b = [5,6,7,8,9,10,11,12,13,14]
    print(unique(a))
    print(intersect(a, b))
    print(union(a, b))
