
def nlogn(n):
    a = 5
    for _ in range(n):
        while n>1:
            a *= 2
            n = n/2
    return a
