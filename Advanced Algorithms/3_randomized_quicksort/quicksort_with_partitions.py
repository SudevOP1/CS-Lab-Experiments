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
    pass

def quicksort_normal_hoare(arr: list):
    pass

def quicksort_randomized_lomuto(arr: list):
    pass

def quicksort_randomized_hoare(arr: list):
    pass

def quicksort_my_method(arr: list):

    # edge case: length < 3
    if len(arr) == 0:
        return arr
    if len(arr) == 1:
        return arr
    if len(arr) == 2:
        if arr[0] < arr[1]:
            return arr
        return [arr[1], arr[0]]

    pivot_index = get_median_pivot_index(arr)
    
    # swap pivot and last elem
    arr[pivot_index], arr[-1] = arr[-1], arr[pivot_index]
    pivot_index = len(arr) - 1

    # keep running loop till correct index of selected pivot is founf
    while True:
        
        left = 0                # 1st elem from left greater than pivot
        right = len(arr) - 2    # 1st elem from right lesser than pivot
        while arr[left] < arr[pivot_index]:
            left += 1
        while arr[right] > arr[pivot_index]:
            right -= 1

        # if left and right dont cross, swap left and right
        if left < right:
            arr[left], arr[right] = arr[right], arr[left]

        # if left and right cross, swap left and pivot
        # and break out of loop (pivot found)
        else:
            arr[left], arr[pivot_index] = arr[pivot_index], arr[left]
            pivot_index = left
            break

    sorted_arr1 = quicksort_my_method(arr[:pivot_index])
    sorted_arr2 = quicksort_my_method(arr[pivot_index + 1:])
    return sorted_arr1 + [arr[pivot_index],] + sorted_arr2

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
    arr = [2, 4, 9, 3, 6, 7, 1, 5, 8, 10]
    print(quicksort(arr, "my_method"))
