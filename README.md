# Proq

Proq - A command line tool for authoring programming questions at scale.

# Terminology

- ProQ or Proq - short for Programming Question present in a structured markdown template.
- Proq file - A structured markdown jinja2 template contains the Proq.
- Nested proq file - An YAML file containing nested structure for creating structured set of proq in multiple levels.


# The proq command line

- **`proq`** - The main command line tool with sub-commands for creating, evaluating and exporting programming questions.

## Subcommands
Use `proq subcommand --help` to know more about the sub-command.

- `proq create` - create a markdown template (proq files) for authoring the programming questions.
- `proq evaluate` - evaluate the test cases configured using the build and compile process defined proq files.
- `proq export` - export a Proq file or a Nested proq file as JSON, html or pdf.

## Quick Start

### Creating a proq
```
proq create -npu 3 -npr 3 --lang c sample.md
```

### Evaluating a proq
```
proq evaluate sample.md
```

### Exporting a proq
```
proq export sample.md -f pdf
```


## Proq File Format

The **Proq File Format** is a structured way to define coding problems, solutions, and test cases using a combination of Markdown-based Jinja templates. This format ensures clarity, flexibility, and compatibility with auto-grading environments. Each file is divided into well-defined sections with specific purposes and annotations.


### File Structure

A Proq file is composed of three main sections:
1. **YAML Header**
2. **Problem Statement**
3. **Solution**
4. **Test Cases**

### 1. YAML Header
The YAML header contains metadata about the problem, such as its title and tags. The `title` and `tags` is defined in the pydantic model. But also support additional tags.

**Example**:
```yaml
---
title: Delete first three elements of a list
tags: ['list','list manipulation','slicing']
---
```


### 2. Problem Statement
This section describes the coding task to be solved, along with examples to clarify the requirements. 


### 3. Solution
The solution is defined in a Markdown code block and annotated with special HTML-like tags to structure the code into editable and non-editable parts.

#### Tag Overview:
- `<prefix>...</prefix>`(Optional):  
  Non-editable code that appears before the main solution.
- `<template>...</template>`:  
  Editable code. Can include:
  - `<sol>...</sol>`: Parts only present in the solution.
  - `<los>...</los>`: Parts only present in the template.
- `<suffix>...</suffix>`(Optional):  
  Non-editable code after the solution.
- `<suffix_invisible>...</suffix_invisible>`(Optional):  
  Non-visible code for additional functionality or testing.

#### Code Block Header

The language specified in the start of the solution code block is considered as the coding language. In addition to the language. The first line also has some arguments that resemble command line arguments of the format `FILE_NAME -r RUN_COMMAND -b BUILD_COMMAND`. This is used for local evaluation of the programming assignments.

**Example**:
````markdown
# Solution

```py3 test.py -r 'python test.py'
<template>
def delete_first_three(l: list) -> None:
    '''
    Given a list, delete the first three elements in the list.

    Arguments:
    l: list - a list of elements.

    Return: None - the list is modified in place.
    '''
    <los>...</los>
    <sol>del l[:3]</sol>
</template>

<suffix_invisible>
{% include '../function_type_and_modify_check_suffix.py.jinja' %}
</suffix_invisible>
```
````



### 4. Test Cases

Test cases verify the solution and are divided into **Public** and **Private** cases. Each case specifies input, the function call, and the expected output. The Test cases will have the following structure. The code blocks inside the second level headings are alternatively assumed to be inputs and outputs. **Each Input and Output header should be unique.**

````markdown

# Public Test Cases

## Input 1
```
Some input
```

## Output 1
```
Some output
```

# Private Test Cases

## Input 1 - With Some info
```
Some hidden input
```

## Output 1 
```
Some hidden output
```
````

