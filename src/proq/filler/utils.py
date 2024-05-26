import re
import bs4
from importlib.resources import files
from marko.ext.gfm import gfm
import html
from jinja2 import Environment, PackageLoader, select_autoescape


math_pattern = re.compile(r'(\$\$)(.*?)\$\$|(\$)(.*?)\$', re.DOTALL)

def to_seek(proq:dict):
    proq = proq.copy()
    include_math =  math_pattern.search(proq["statement"])
    include_hjs = bs4.BeautifulSoup(proq["statement"],features="html.parser").select_one("pre code")
    if include_math:
        proq["statement"] = math_pattern.sub(
            lambda x: f"{(x.group(1) or x.group(3))}{html.unescape(x.group(2) or x.group(4))}{x.group(1) or x.group(3)}",
            proq["statement"]
        )
    env = Environment(
        loader=PackageLoader("proq", "templates"),
        autoescape=select_autoescape()
    )
    env.filters["gfm"] = gfm.convert
    template = env.get_template('seek_template.html.jinja')
    return template.render(proq=proq,include_math=include_math,include_hjs=include_hjs)
    

def decomment(string):
    string = re.sub("#.*", "", string)
    string = re.sub("\n[\n]+", "\n\n", string, re.DOTALL)
    return string
