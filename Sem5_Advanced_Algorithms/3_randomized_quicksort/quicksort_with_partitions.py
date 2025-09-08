import random

# helper function
def get_median_pivot_index(arr: list):
    index1 = 0
    index2 = len(arr) // 2
    index3 = len(arr) - 1

    if arr[index1] <= arr[index2] <= arr[index3] or arr[index3] <= arr[index2] <= arr[index1]:
        return index2
    elif arr[index2] <= arr[index1] <= arr[index3] or arr[index3] <= arr[index1] <= arr[index2]:
        return index1
    return index3

def quicksort_normal_lomuto(arr: list):
    if len(arr) <= 1:
        return arr

    i = -1
    j = 0
    p = len(arr) - 1

    while j < p:
        if arr[j] < arr[p]:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
        j += 1
    arr[i + 1], arr[p] = arr[p], arr[i + 1]
    p = i + 1

    sorted_arr1 = quicksort_normal_lomuto(arr[:p])
    sorted_arr2 = quicksort_normal_lomuto(arr[p + 1:])
    return sorted_arr1 + [arr[p],] + sorted_arr2

def quicksort_normal_hoare(arr: list):
    if len(arr) <= 1:
        return arr
    
    i = -1
    j = len(arr)
    p = 0

    while True:
        # move i to right until >= pivot
        i += 1
        while arr[i] < arr[p]:
            i += 1
        
        # move j to left until <= pivot
        j -= 1
        while arr[j] > arr[p]:
            j -= 1

        if i >= j:
            arr[j], arr[p] = arr[p], arr[j]
            p = j
            break
        arr[i], arr[j] = arr[j], arr[i]

    sorted_arr1 = quicksort_normal_hoare(arr[:p])
    sorted_arr2 = quicksort_normal_hoare(arr[p + 1:])
    return sorted_arr1 + [arr[p],] + sorted_arr2

def quicksort_randomized_lomuto(arr: list):
    pass

def quicksort_randomized_hoare(arr: list):
    pass

def quicksort_my_method(arr: list):

    # edge case: length < 3
    if len(arr) <= 1:
        return arr
    if len(arr) == 2:
        return arr if arr[0] <= arr[1] else [arr[1], arr[0]]

    pivot_ind = get_median_pivot_index(arr)
    arr[pivot_ind], arr[-1] = arr[-1], arr[pivot_ind]
    pivot_val = arr[-1]

    left = -1
    for right in range(len(arr) - 1):
        if arr[right] < pivot_val:
            left += 1
            arr[left], arr[right] = arr[right], arr[left]
    arr[left + 1], arr[-1] = arr[-1], arr[left + 1]
    pivot_ind = left + 1

    sorted_arr1 = quicksort_my_method(arr[:pivot_ind])
    sorted_arr2 = quicksort_my_method(arr[pivot_ind+1:])
    return sorted_arr1 + [arr[pivot_ind]] + sorted_arr2

def quicksort(arr: list, partition_type: str):
    """
    partition_types:
        normal lomuto
        normal hoare
        randomized lomuto
        randomized hoare
        my method
    """
    if partition_type == "normal_lomuto":       return quicksort_normal_lomuto(arr)
    if partition_type == "normal_hoare":        return quicksort_normal_hoare(arr)
    if partition_type == "randomized_lomuto":   return quicksort_randomized_lomuto(arr)
    if partition_type == "randomized_hoare":    return quicksort_randomized_hoare(arr)
    if partition_type == "my_method":           return quicksort_my_method(arr)
    raise Exception("Invalid partition_type")

if __name__ == "__main__":
    arr = [4, 10, 9, 4, 8, 0, 6, 0, 10, 4]
    partition_types = [
        "normal_lomuto    ",
        "normal_hoare     ",
        "randomized_lomuto",
        "randomized_hoare ",
        "my_method        ",
    ]
    
    print()
    print(arr)
    for p in partition_types:
        print(f"{p} : {str(quicksort(arr, p.strip()))}")
    print()
