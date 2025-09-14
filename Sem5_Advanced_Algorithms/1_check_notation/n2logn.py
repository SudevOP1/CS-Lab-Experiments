
def n2logn(n):
    a = 5
    for _ in range(n):
        for _ in range(n):
            while n>1:
                a *= 2
                n = n/2
        for _ in range(n):
            a -= 10
    return a
