---
title: Problem 4 - Fibonacci Sequence Generation
---

# Problem Statement

Create a function that generates all Fibonacci numbers less than or equal to a specified limit. The result should be returned as a list of numbers.

# Solution

```py3
def generate_fibonacci(limit):
    if limit < 0:
        return []
    sequence = [0, 1]
    while sequence[-1] + sequence[-2] <= limit:
        sequence.append(sequence[-1] + sequence[-2])
    return sequence[:-1] if limit < 1 else sequence
```

# Public Test Cases

## Input 1

```
is_equal(
    generate_fibonacci(15),
    [0, 1, 1, 2, 3, 5, 8, 13]
)
```

## Output 1

```
[0, 1, 1, 2, 3, 5, 8, 13]
```

## Input 2

```
is_equal(
    generate_fibonacci(1),
    [0, 1, 1]
)
```

## Output 2

```
[0, 1, 1]
```

# Private Test Cases

## Input 1

```
limit = 30
is_equal(
    generate_fibonacci(limit),
    [0, 1, 1, 2, 3, 5, 8, 13, 21]
)
limit = -2
is_equal(
    generate_fibonacci(limit),
    []
)
```

## Output 1

```
[0, 1, 1, 2, 3, 5, 8, 13, 21]
[]
```
