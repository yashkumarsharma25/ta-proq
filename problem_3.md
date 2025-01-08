
---
title: Problem 3 - Second Highest Unique Number
---

# Problem Statement

Write a Python function that reads a list of integers from the input and prints the second highest unique number in the list. If the list has fewer than two unique numbers, print 'None'.

# Solution

```py3
def find_second_highest():
    numbers = list(map(int, input().split()))
    unique_numbers = list(set(numbers))
    if len(unique_numbers) < 2:
        print(None)
    else:
        unique_numbers.sort(reverse=True)
        print(unique_numbers[1])
```

# Public Test Cases

## Input 1

```
is_equal(
    find_second_highest([4, 2, 9, 5, 9]),
    5
)
```

## Output 1

```
5
```

## Input 2

```
is_equal(
    find_second_highest([3, 3, 3]),
    None
)
```

## Output 2

```
None
```

# Private Test Cases

## Input 1

```
numbers = [12, 45, 45, 67, 89]
is_equal(
    find_second_highest(numbers),
    67
)
numbers = [100]
is_equal(
    find_second_highest(numbers),
    None
)
```

## Output 1

```
67
None
```
