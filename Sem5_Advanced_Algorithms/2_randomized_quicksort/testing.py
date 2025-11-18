import random, time, json
from quicksort_with_partitions import quicksort

partition_types = [
    "normal_lomuto    ",
    "normal_hoare     ",
    "my_method        ",
    "random_lomuto    ",
    "random_hoare     ",
]

def generate_random_arr(n):
    return [random.randint(0, n) for _ in range(n)]

def test_random(num_tries: int, num_elems: int):
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

def test_3(num_tries: int, num_elems: int):
    times = {}
    for _ in range(num_tries):
        rand_arr = generate_random_arr(num_elems)
        
        for type, arr in {
            "sorted": sorted(rand_arr),
            "random": rand_arr,
            "descending": sorted(rand_arr[::-1]),
        }.items():
            times[type] = {} if type not in times.keys() else times[type]
            for p in partition_types:
                t1 = time.time()
                sorted_arr = quicksort(arr, p.strip())
                t2 = time.time()
                times[type][p] = 0 if p not in times[type].keys() else times[type][p]
                times[type][p] += (t2 - t1)
    
    print(f"total seconds for {num_elems} elements across {num_tries} tries:")
    print(json.dumps(times, indent=2))
        

if __name__ == "__main__":
    
    # test_random(10000, 100)
    test_3(10000, 100)
