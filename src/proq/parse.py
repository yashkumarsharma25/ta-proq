from md2json import dictify
from marko import Markdown
import yaml
import os
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

def clip_extra_lines(text:str)->str:
    """
    Reduces sequences of more than two consecutive line breaks 
    to exactly two line breaks.
    Also strip blank lines in the begining.
    """
    return re.sub(r'\n\s*\n', '\n\n', text,flags=re.DOTALL)



def get_tag_content(tag:str, html:str)->str:
    """Get the inner html of first match of a tag.
    Returns empty string if tag not found
    """
    content = re.findall(
        f"<{re.escape(tag)}>(.*?)</{re.escape(tag)}>", html, re.DOTALL
    )
    content = clip_extra_lines(content[0]) if content else ""
    return content

def remove_all_matching_tags(tag, html):
    return re.sub(
        f"<{re.escape(tag)}>(.*?)</{re.escape(tag)}>", "", html, flags=re.DOTALL
    )

def strip_tags(html: str) -> str:
    """Removes all tags from an HTML text."""
    return re.sub(r'<\/?.*?>', "", html,flags=re.DOTALL)


def extract_solution(solution):
    code = {}
    solution = extract_codeblock_content(solution)
    code_parts = ["prefix", "suffix", "suffix_invisible","template"]
    for part in code_parts:
        code[part] = get_tag_content(part, solution)
        # remove if only white space 
        if code[part].strip() == "": 
            code[part] = ""
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


def proq_to_json(proq_file) -> tuple[str, dict]:
    """Loads the proq file and returns a tuple (unit_name, proq_data)
    """
    from jinja2 import Environment, FileSystemLoader, select_autoescape
    env = Environment(
        loader=FileSystemLoader(os.path.abspath(os.path.dirname(proq_file))),
        autoescape=select_autoescape()
    )
    template = env.get_template(os.path.basename(proq_file))
    raw_content = template.render()
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
    return unit_name, problems