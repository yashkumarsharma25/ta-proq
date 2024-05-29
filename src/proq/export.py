from .parse import proq_to_json
import json
import os
import argparse
from marko.ext.gfm import gfm

import asyncio
from playwright.async_api import async_playwright
from importlib.resources import files

async def print_html_to_pdf(html_content, output_pdf_path):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context()
        page = await context.new_page()
        await page.set_content(html_content)
        await page.pdf(path=output_pdf_path, print_background=True)
        await browser.close()

def get_template(template):
    return files("proq").joinpath("templates").joinpath(template).read_text()

def get_rendered_html(unit_name, proq_data):
    from jinja2 import Environment, FunctionLoader, select_autoescape
    env = Environment(
        loader=FunctionLoader(get_template),
        autoescape=select_autoescape()
    )
    template = env.get_template('proq_template.html.jinja')
    for problem in proq_data:
        problem["statement"] = gfm.convert(problem["statement"])
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
