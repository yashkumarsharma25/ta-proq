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


def extract_solution(solution):
    code = {}
    solution = extract_codeblock_content(solution)
    code_parts = ["prefix", "suffix", "suffix_invisible","template"]
    for part in code_parts:
        code[part] = re.findall(
            f"<{re.escape(part)}>(.*?)</{re.escape(part)}>", solution, re.DOTALL
        )
        code[part] = code[part][0].strip("\n") if code[part] else ""
    code["solution"] = str(code["template"])
    # in template remove sol and solution tag content and remove placeholder and ph tags
    code["solution"] = re.sub(r'<\/?solution>',"",code["solution"])
    code["solution"] = re.sub("<solution>(.*?)</solution>", "", code["solution"], flags=re.DOTALL)
    code["template"] = re.sub(
        "<solution>(.*?)</solution>", "", code["template"], flags=re.DOTALL
    )
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
