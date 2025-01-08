---
title: Problem 2 - Palindrome Check
---

# Problem Statement

Create a function in Python that checks whether a given string is a palindrome. The function should ignore spaces, punctuation, and case differences.

# Solution

```py3
def check_palindrome(text):
    clean_text = ''.join(char.lower() for char in text if char.isalnum())
    return clean_text == clean_text[::-1]
```

# Public Test Cases

## Input 1

```
is_equal(
    check_palindrome("Madam, in Eden, I'm Adam"),
    True
)
```

## Output 1

```
True
```

## Input 2

```
is_equal(
    check_palindrome("Python"),
    False
)
```

## Output 2

```
False
```

# Private Test Cases

## Input 1

```
text = "Step on no pets"
is_equal(
    check_palindrome(text),
    True
)
text = "Palindrome"
is_equal(
    check_palindrome(text),
    False
)
```

## Output 1

```
True
False
```
