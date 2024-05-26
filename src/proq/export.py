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

def clip_extra_lines(text:str)->str:
    """
    Reduces sequences of more than two consecutive line breaks 
    to exactly two line breaks.
    Also strip blank lines in the begining.
    """
    return re.sub(r'\n\s*\n', '\n\n', text,flags=re.DOTALL).strip("\n")


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

import os
import argparse

import asyncio
from playwright.async_api import async_playwright

async def print_html_to_pdf(html_content, output_pdf_path):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context()
        page = await context.new_page()
        await page.set_content(html_content)
        await page.pdf(path=output_pdf_path, print_background=True)
        await browser.close()

def get_rendered_html(unit_name, proq_data):
    from jinja2 import Environment, PackageLoader, select_autoescape
    env = Environment(
        loader=PackageLoader("proq_filler", "templates"),
        autoescape=select_autoescape()
    )
    template = env.get_template('proq_template.html.jinja')
    for problem in proq_data:
        from .utils import md2seek
        problem["statement"] = md2seek(problem["statement"])
    return template.render(unit_name = unit_name,problems = proq_data)

def proq_export(proq_file,output_file=None,format="json"):
    if not os.path.isfile(proq_file):
        raise FileNotFoundError(f"{proq_file} is not a valid file")
    
    if not output_file:
        assert format in ["json","html","pdf"], "Export format not valid. Supported formats are json and html."
        output_file = ".".join(proq_file.split(".")[:-1])+f".{format}"
        
    unit_name, proq_data = proq_to_json(proq_file)
    with open(output_file, "w") as f:
        if format == "json":
            json.dump(proq_data, f, indent=2)
        elif format == "html":
            with open(output_file,"w") as f:
                f.write(get_rendered_html(unit_name, proq_data))
        elif format == "pdf":
            asyncio.run(print_html_to_pdf(get_rendered_html(unit_name, proq_data), output_file))

    print(f"Proqs dumped to {output_file}")
    

def conifgure_cli_parser(parser:argparse.ArgumentParser):
    parser.add_argument("proq_file", metavar="F", type=str, help="proq file to be exported")
    parser.add_argument("-o","--output-file",metavar="OUTPUT_FILE", required=False, type=str, help="name of the output file.")
    parser.add_argument("-f","--format", metavar="OUTPUT_FORMAT", choices=['json', 'html', "pdf"], default="json", help="format of the output file export")
    parser.set_defaults(func=lambda args: proq_export(args.proq_file,args.output_file,args.format))
