import sys
import random

sys.setrecursionlimit(10000)


class Counter:
    def __init__(self):
        self.value = 0

    def add(self):
        self.value += 1


def insertion_sort(arr, left, right, counter):
    # insertion sort for the smaller subarrays
    for i in range(left + 1, right + 1):
        key = arr[i]
        j = i - 1

        while j >= left:
            counter.add()

            if arr[j] > key:
                arr[j + 1] = arr[j]
                j -= 1
            else:
                break

        arr[j + 1] = key


def merge(arr, temp, left, mid, right, counter):
    i = left
    j = mid + 1
    k = left

    # compare elements from both halves
    while i <= mid and j <= right:
        counter.add()

        if arr[i] <= arr[j]:
            temp[k] = arr[i]
            i += 1
        else:
            temp[k] = arr[j]
            j += 1

        k += 1

    # copy any remaining elements
    while i <= mid:
        temp[k] = arr[i]
        i += 1
        k += 1

    while j <= right:
        temp[k] = arr[j]
        j += 1
        k += 1

    # copy the merged section back into arr
    for i in range(left, right + 1):
        arr[i] = temp[i]


def hybrid_sort(arr, temp, left, right, S, counter):
    # use insertion sort once the subarray becomes small enough
    size = right - left + 1

    if size <= S:
        insertion_sort(arr, left, right, counter)
        return

    mid = (left + right) // 2

    hybrid_sort(arr, temp, left, mid, S, counter)
    hybrid_sort(arr, temp, mid + 1, right, S, counter)

    merge(arr, temp, left, mid, right, counter)


def merge_sort(arr, temp, left, right, counter):
    if left >= right:
        return
    mid = (left + right) // 2
    merge_sort(arr, temp, left, mid, counter)
    merge_sort(arr, temp, mid + 1, right, counter)
    merge(arr, temp, left, mid, right, counter)


def run_hybrid_sort(arr, S):
    a = arr[:]
    temp = [0] * len(a)
    counter = Counter()
    if len(a) > 0:
        hybrid_sort(a, temp, 0, len(a) - 1, S, counter)
    return counter.value


def run_merge_sort(arr):
    a = arr[:]
    temp = [0] * len(a)
    counter = Counter()
    if len(a) > 0:
        merge_sort(a, temp, 0, len(a) - 1, counter)
    return counter.value


def generate_random_array(n, seed=42):
    rng = random.Random(seed)
    return [rng.randint(1, n) for _ in range(n)]
