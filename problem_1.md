---
title: Problem 1 - Factorial Calculation
---

# Problem Statement

Write a function in Python that calculates the factorial of a given non-negative integer using recursion. The function must handle invalid inputs and return an error message if the input is not a non-negative integer.

# Solution

```py3
def compute_factorial(n):
    if not isinstance(n, int) or n < 0:
        return 'Error: Input must be a non-negative integer.'
    if n == 0:
        return 1
    return n * compute_factorial(n - 1)
```

# Public Test Cases

## Input 1

```
is_equal(
    compute_factorial(3),
    6
)
```

## Output 1

```
6
```

## Input 2

```
is_equal(
    compute_factorial(0),
    1
)
```

## Output 2

```
1
```

# Private Test Cases

## Input 1

```
n = 7
is_equal(
    compute_factorial(n),
    5040
)
n = -5
is_equal(
    compute_factorial(n),
    'Error: Input must be a non-negative integer.'
)
```

## Output 1

```
5040
'Error: Input must be a non-negative integer.'
```
