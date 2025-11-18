
def n3(n):
    a = 5
    for i in range(n):
        a += 1
        for j in range(n):
            a += 1
            for k in range(n):
                a += 1
    for k in range(n):
        a += 1
    return a

