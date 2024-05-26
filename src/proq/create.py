#!/usr/bin/env python
import argparse

sample_yaml_headers = {}
sample_yaml_headers["python"]="""---
lang: python
local_evaluate:
    source_file: test.py
    build: ""
    run: python test.py
seek_config:
    lang : Python3
    deadline : 09/28/2023,23:59 # mm/dd/yyyy,HH:MM
    evaluator": nsjail
    evaluator_type: Test Cases
    ignore_presentation_error": true
    allow_compile": true
    show_sample_solution": true
    is_public: false
---
"""

sample_yaml_headers["java"]="""---
lang: java
local_evaluate:
    source_file: Test.java
    build: javac Test.java
    run: java Test.class
seek_config:
    lang : Java
    deadline : 09/28/2023,23:59 # mm/dd/yyyy,HH:MM
    evaluator": nsjail
    evaluator_type: Test Cases
    ignore_presentation_error": true
    allow_compile": true
    show_sample_solution": true
    is_public: false
    solution_file: Main.java
---
"""

solution_content="""
```{}
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

import os
def generate_template(output_file,lang,num_problems, num_public, num_private, pattern):
    if os.path.isfile(output_file):
        raise FileExistsError("A file with the same name already exists.")
    
    with open(output_file, "w") as file:
        file.write(sample_yaml_headers.get(lang,sample_yaml_headers["python"]))        
        file.write(f"\n# Unit Name\n\n")

        for problem_num in range(1, num_problems + 1):
            file.write(f"## {pattern.format(problem_num)}\n\n")
            file.write(f"### Problem Statement\n\n")
            file.write(f"### Solution{solution_content.format(lang)}\n")
            file.write(f"### Testcases\n\n")

            file.write(f"#### Public Testcases\n\n")
            for public_testcase_num in range(1, num_public + 1):
                file.write(f"##### Input {public_testcase_num}\n\n```\n\n```\n\n")
                file.write(f"##### Output {public_testcase_num}\n\n```\n\n```\n\n")

            file.write(f"#### Private Testcases\n\n")
            for private_testcase_num in range(1, num_private + 1):
                file.write(f"##### Input {private_testcase_num}\n\n```\n\n```\n\n")
                file.write(f"##### Output {private_testcase_num}\n\n```\n\n```\n\n")


def configure_cli_parser(parser:argparse.ArgumentParser):
    parser.add_argument(
        "-o",
        "--output-file",
        type=str,
        help="Output file name",
        default="proq_template.md",
    )
    parser.add_argument(
        "-l", "--lang", type=str, help="Language of the proq", default="python"
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
    parser.set_defaults(
        func = lambda args: generate_template(
            args.output_file,
            args.lang,
            args.num_problems,
            args.num_public,
            args.num_private,
            args.pattern
        )
    )
