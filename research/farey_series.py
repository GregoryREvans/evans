class Term:

    # Constructor to initialize
    # x and y in x/y
    def __init__(self, x, y):
        self.x = x
        self.y = y


# GCD of a and b
def gcd(a, b):
    if b == 0:
        return a
    return gcd(b, a % b)


# Function to print
# Farey sequence of order n
def farey(n):

    # Create a vector to
    # store terms of output
    v = []

    # One by one find and store
    # all terms except 0/1 and n/n
    # which are known
    for i in range(1, n + 1):
        for j in range(i + 1, n + 1):

            # Checking whether i and j
            # are in lowest term
            if gcd(i, j) == 1:
                v.append(Term(i, j))

    # Sorting the term of sequence
    for i in range(len(v)):
        for j in range(i + 1, len(v)):
            if v[i].x * v[j].y > v[j].x * v[i].y:
                v[i], v[j] = v[j], v[i]

    # Explicitly printing first term
    print("0/1", end=" ")

    # Printing other terms
    for i in range(len(v)):
        print("%d/%d" % (v[i].x, v[i].y), end=" ")

    # explicitly printing last term
    print("1/1")


n = 23
print("Farey sequence of order %d is" % n)
farey(n)
