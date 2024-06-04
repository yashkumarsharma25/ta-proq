#!/usr/bin/env python
import argparse
import os
from datetime import datetime,timedelta
from .template_utils import package_env

default_lang_config = {
    "python": {
        "lang": "python",
        "source_file": "test.py",
        "build": "",
        "run": "python test.py",
        "seek_lang": "Python3",
    },
    "java": {
        "lang": "java",
        "source_file": "Test.java",
        "build": "javac Test.java",
        "run": "java Test.class",
        "seek_lang": "Java",
        "solution_file": "Test.java"
    },
    "c":{
        "lang": "c",
        "source_file": "test.c",
        "build": "gcc test.c -Winfo ",
        "run": "java Test.class",
        "seek_lang": "C",
    }
}


def generate_template(output_file,lang,num_problems, num_public, num_private, pattern):
    if os.path.isfile(output_file):
        raise FileExistsError("A file with the same name already exists.")
    
    template = package_env.get_template('proq_template.md.jinja')
    unknown_lang_config = {
        "lang":lang,
        "source_file":"",
        "build":"",
        "run":"",
        "seek_lang":""
    }
    # deadline is 10 days after the date of creation by default
    deadline = (datetime.today()+timedelta(days=10)).strftime("%m/%d/%y:23:59")
    content = template.render(
        **default_lang_config.get(lang,unknown_lang_config),
        num_problems=num_problems,
        num_public=num_public,
        num_private=num_private,
        pattern=pattern, 
        deadline=deadline
    )
    with open(output_file,"w") as f:
        f.write(content)

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
