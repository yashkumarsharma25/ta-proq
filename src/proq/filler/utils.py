import re

from ..template_utils import package_env

math_pattern = re.compile(r'(\$\$)(.*?)\$\$|(\$)(.*?)\$', re.DOTALL)

code_block_pattern = re.compile("```")

def to_seek(proq:dict):
    proq = proq.copy()
    include_math =  math_pattern.search(proq["statement"]) is not None
    include_hjs = code_block_pattern.search(proq["statement"]) is not None

    # if include_math:
        # proq["statement"] = math_pattern.sub(
        #     lambda x: f"{(x.group(1) or x.group(3))}{html.unescape(x.group(2) or x.group(4))}{x.group(1) or x.group(3)}",
        #     proq["statement"]
        # )    
    template = package_env.get_template('seek_template.html.jinja')
    return template.render(proq=proq,include_math=include_math,include_hjs=include_hjs)
    

def decomment(string):
    string = re.sub("#.*", "", string)
    string = re.sub("\n[\n]+", "\n\n", string, re.DOTALL)
    return string
