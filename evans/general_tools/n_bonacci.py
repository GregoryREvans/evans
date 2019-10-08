def n_bonacci(n, m, first=1):
    final = []
    a = [0] * m
    a[n - 1] = first
    for i in range(n, m):
        for j in range(i - n, i):
            a[i] = a[i] + a[j]
    for i in range(0, m):
        final.append(a[i])
    for i in range(n - 1):
        final.remove(0)
    return final


print(n_bonacci(n=2, m=15, first=1))
