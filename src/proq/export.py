from .parse import load_proq, ProqSet
import json
import os
import argparse

import asyncio
from playwright.async_api import async_playwright
from .template_utils import package_env

async def print_html_to_pdf(html_content, output_pdf_path):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context()
        page = await context.new_page()
        await page.set_content(html_content)
        await page.pdf(path=output_pdf_path, print_background=True)
        await browser.close()


def get_rendered_html(proq:ProqSet):
    template = package_env.get_template('proq_export_template.html.jinja')
    return template.render(unit_name = proq.unit_name, problems = proq.problems)

def proq_export(proq_file,output_file=None,format="json"):
    if not os.path.isfile(proq_file):
        raise FileNotFoundError(f"{proq_file} is not a valid file")
    
    if not output_file:
        assert format in ["json","html","pdf"], "Export format not valid. Supported formats are json and html."
        output_file = ".".join(proq_file.split(".")[:-1])+f".{format}"
        
    proq = load_proq(proq_file)
    with open(output_file, "w") as f:
        if format == "json":
            json.dump(proq.problems, f, indent=2)
        elif format == "html":
            with open(output_file,"w") as f:
                f.write(get_rendered_html(proq))
        elif format == "pdf":
            asyncio.run(print_html_to_pdf(get_rendered_html(proq), output_file))

    print(f"Proqs dumped to {output_file}")
    

def conifgure_cli_parser(parser:argparse.ArgumentParser):
    parser.add_argument("proq_file", metavar="F", type=str, help="proq file to be exported")
    parser.add_argument("-o","--output-file",metavar="OUTPUT_FILE", required=False, type=str, help="name of the output file.")
    parser.add_argument("-f","--format", metavar="OUTPUT_FORMAT", choices=['json', 'html', "pdf"], default="json", help="format of the output file export")
    parser.set_defaults(func=lambda args: proq_export(args.proq_file,args.output_file,args.format))
