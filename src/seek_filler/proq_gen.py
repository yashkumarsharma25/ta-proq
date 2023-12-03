#!/usr/bin/env python
import argparse

yaml_header_sample="""---
local_evaluate:
    file_name: test.py
    build: ""
    run: python test.py
lang : "Python3"
# mm/dd/yyyy,HH:MM
deadline : "09/28/2023,23:59"
evaluator": "nsjail"
ignore_presentation_error": true
allow_compile": true
show_sample_solution": true
---
"""

solution_content="""
```
<prefix>

</prefix>
<template>

<solution>

</solution>
</template>
<suffix>

</suffix>
<suffix_invisible>

</suffix_invisible>
```
"""

def generate_template(output_file, num_problems, num_public, num_private, pattern):
    with open(output_file, "w") as file:
        file.write(yaml_header_sample)        
        for problem_num in range(1, num_problems + 1):
            file.write(f"# Unit Name\n\n")
            file.write(f"## {pattern.format(problem_num)}\n\n")
            file.write(f"### Problem Statement\n\n")
            file.write(f"### Solution{solution_content}\n")
            file.write(f"### Testcases\n\n")

            file.write(f"#### Public Testcases\n\n")
            for public_testcase_num in range(1, num_public + 1):
                file.write(f"##### Input {public_testcase_num}\n\n```\n\n```\n\n")
                file.write(f"##### Output {public_testcase_num}\n\n```\n\n```\n\n")

            file.write(f"#### Private Testcases\n\n")
            for private_testcase_num in range(1, num_private + 1):
                file.write(f"##### Input {private_testcase_num}\n\n```\n\n```\n\n")
                file.write(f"##### Output {private_testcase_num}\n\n```\n\n```\n\n")


def main():
    parser = argparse.ArgumentParser(description="Generate a template for problems")
    parser.add_argument(
        "-o",
        "--output-file",
        type=str,
        help="Output file name",
        default="proq_template.md",
    )
    parser.add_argument(
        "-np", "--num-problems", type=int, help="Number of problems", default=5
    )
    parser.add_argument(
        "-npu", "--num-public", type=int, help="Number of public test cases", default=5
    )
    parser.add_argument(
        "-npr",
        "--num-private",
        type=int,
        help="Number of private test cases",
        default=5,
    )
    parser.add_argument(
        "--pattern", type=str, help="Problem numbering pattern", default="Problem {}"
    )

    args = parser.parse_args()
    generate_template(**vars(args))


if __name__ == "__main__":
    main()
