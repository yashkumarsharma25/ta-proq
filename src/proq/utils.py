import re
import bs4
import subprocess
from importlib.resources import files
from marko.ext.gfm import gfm
import html


math_pattern = re.compile(r'(\$\$)(.*?)\$\$|(\$)(.*?)\$', re.DOTALL)

hljs_include = """
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/nnfx-light.min.css" 
integrity="sha512-ZjzFgTdefwbr872DItYgMHB53Fz62tfzctEwMJJ05aDtyK1MUy61NXs57QFqVKOeJsn8BMvDMjRhhALXLDz1lw==" 
crossorigin="anonymous" referrerpolicy="no-referrer" />

<script >
function require(url, callback) 
{
  var e = document.createElement("script");
  e.src = url;
  e.type="text/javascript";
  e.addEventListener('load', callback);
  document.getElementsByTagName("head")[0].appendChild(e);
}

require("https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js", function() { 
   hljs.highlightAll()
});
</script>
"""

def md2seek(markdown, includes=None):
    if not includes:
        includes = []

    result = gfm.convert(markdown)
    result = f'<div class="prob-statement">\n{result}\n</div>'
    if "style" in includes:
        with files("proq").joinpath("templates/style.css").open("r") as f:
            result = f"<style>{f.read()}</style>\n" + result
    if "highlight" in includes:
        if bs4.BeautifulSoup(result,features="html.parser").select_one("pre code"):
            result = hljs_include  + result
    if "math" in includes:
        if math_pattern.search(result):
            math_pattern.sub(
                lambda x: f"{(x.group(1) or x.group(3))}{html.unescape(x.group(2) or x.group(4))}{x.group(1) or x.group(3)}",
                result
            )
            with files("proq").joinpath("templates/katex_includes.html").open("r") as f:
                katex_include = f.read()
            result = katex_include + result
    
    return result


def decomment(string):
    string = re.sub("#.*", "", string)
    string = re.sub("\n[\n]+", "\n\n", string, re.DOTALL)
    return string
