import random, time
from quicksort_with_partitions import quicksort

def generate_random_arr(n):
    return [random.randint(0, n) for i in range(n)]

num_tries = 100
num_elems = 100
partition_types = [
    "normal_lomuto    ",
    "normal_hoare     ",
    "my_method        ",
    "random_lomuto    ",
    "random_hoare     ",
]

if __name__ == "__main__":
    times = {}
    for p in partition_types:
        times[p] = []

    for i in range(num_tries):
        unsorted_arr = generate_random_arr(num_elems)
        # print(unsorted_arr)
        for p in partition_types:
            t1 = time.time()
            arr = quicksort(unsorted_arr, p.strip())
            t2 = time.time()
            times[p].append(t2 - t1)
        # print(f"test no. {i} done")
    
    print()
    print(f"total seconds for {num_elems} elements across {num_tries} tries:")
    for p in partition_types:
        print(f"{p} : {sum(times[p]):.5f}")
    print()



