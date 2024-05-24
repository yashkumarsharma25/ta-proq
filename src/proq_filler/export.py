from md2json import dictify
from marko import Markdown
import yaml
import json
import re


def extract_codeblock_content(text):
    return (
        [
            block
            for block in Markdown().parse(text).children
            if (block.get_type() == "FencedCode" or block.get_type() == "CodeBlock")
        ][0]
        .children[0]
        .children
    )


def get_tag_content(tag:str, html:str)->str:
    """Get the inner html of first match of a tag.
    Returns empty string if tag not found
    """
    content = re.findall(
        f"<{re.escape(tag)}>(.*?)</{re.escape(tag)}>", html, re.DOTALL
    )
    content = content[0].strip("\n") if content else ""
    return content

def remove_all_matching_tags(tag, html):
    return re.sub(
        f"<{re.escape(tag)}>(.*?)</{re.escape(tag)}>", "", html, flags=re.DOTALL
    )

def strip_tags(html: str) -> str:
    """Removes all tags from an HTML text."""
    return re.sub(r'<\/?.*?>', "", html,flags=re.DOTALL)

def clip_extra_lines(text:str)->str:
    """
    Reduces sequences of more than two consecutive line breaks 
    to exactly two line breaks.
    Also strip blank lines in the begining.
    """
    return re.sub(r'\n\s*\n', '\n\n', text,flags=re.DOTALL).lstrip()

def extract_solution(solution):
    code = {}
    solution = extract_codeblock_content(solution)
    code_parts = ["prefix", "suffix", "suffix_invisible","template"]
    for part in code_parts:
        code[part] = get_tag_content(part, solution)
    code["solution"] = str(code["template"])

    for tag in ["solution","sol"]:
        code["template"] = remove_all_matching_tags(tag, code["template"])
    
    code["solution"] = clip_extra_lines(strip_tags(code["solution"]))
    return code


def extract_testcases(testcases_dict):
    testcases_list = list(testcases_dict.values())
    testcases = []
    for input, output in zip(testcases_list[::2], testcases_list[1::2]):
        testcases.append(
            {
                "input": extract_codeblock_content(input),
                "output": extract_codeblock_content(output),
            }
        )
    return testcases


def proq_to_json(proq_file, to_file=False):
    with open(proq_file) as f:
        raw_content = f.read()
        _, yaml_header, markdown = raw_content.split("---", 2)
        markdown_content = dictify(markdown)
        yaml_header = yaml.safe_load(yaml_header)
    unit_name, problems = markdown_content.popitem()
    problem_names = list(problems.keys())
    for problem_name in problem_names:
        problem = problems[problem_name]
        problem["title"] = problem_name
        problem["statement"] = problem.pop("Problem Statement")
        problem["code"] = extract_solution(problem.pop("Solution"))
        problem["testcases"] = problem.pop("Testcases")
        problem["testcases"]["public_testcases"] = extract_testcases(
            problem["testcases"].pop("Public Testcases")
        )
        problem["testcases"]["private_testcases"] = extract_testcases(
            problem["testcases"].pop("Private Testcases")
        )
        problem.update(yaml_header)
    problems = list(problems.values())
    if to_file:
        with open(f"{unit_name}.json", "w") as f:
            json.dump(problems, f, indent=2)
        print(f"Proqs dumped to {unit_name}.json")
    return unit_name, problems

import os
import argparse


# To html not implemented yet
def proq_export(files):
    for f in files:
        try:
            assert os.path.isfile(f), f"{f} is not a valid file"
            proq_to_json(f, to_file=True)
        except AssertionError as e:
            print(e)

def conifgure_cli_parser(parser):
    parser.add_argument("files", metavar="F", type=str, nargs="+", help="files to be exported")
    parser.set_defaults(func=lambda args: proq_export(args.files))
