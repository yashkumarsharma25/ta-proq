---
lang : "Python3"
# mm/dd/yyyy,HH:MM
deadline : "09/28/2023,23:59"
evaluator": "nsjail"
ignore_presentation_error": true
allow_compile": true
show_sample_solution": true
---

# Unit Name

## Problem Name

### Problem Statement

Sample problem statement containing inline math $x^2$ and some inline code `code` and some block math formulas:

- sample list
  - nested one
  - another on
- sample two
    - lkjdsf

$$
\begin{align*}
    x^2+y^2 &= 3^2+5^2\\
    &=9+16\\
    &= 25
\end{align*}
$$

Some sample code block
```python
printf("hello world")
```
And some Tables

| Column 1 | Column 2 |
| -------- | -------- |
| entry 1  | entry 2  |

- [ ] check 1
- [x] checked

### Solution

```python
<prefix>
import math
</prefix>
<template>
def cube(x):
<solution>
    # just a comment
    return  x**3
</solution>
# comments after solution
</template>
<suffix>
# just a comment
</suffix>
<suffix_invisible>
if __name__ == "__main__":
    print(cube(int(input())))
</suffix_invisible>
```

### Testcases

#### Public Testcases

##### Input 1
```
3
```
##### Output 1
```
27
```

#### Private Testcases

##### Input 1
```
5
```
##### Output 1
```
125
```

## Problem Name 2

### Problem Statement

statement

### Solution

```python
<prefix>
import math
</prefix>
<template>
def cube(x):
<solution>
    # just a comment
    return  x**3
</solution>
# comments after solution
</template>
<suffix>
# just a comment
</suffix>
<suffix_invisible>
if __name__ == "__main__":
    print(cube(int(input())))
</suffix_invisible>
```

### Testcases

#### Public Testcases

##### Input 1
```
3
```
##### Output 1
```
27
```

#### Private Testcases

##### Input 1
```
5
```
##### Output 1
```
125
```


