import re
import bs4
import subprocess
from importlib.resources import files
from marko.ext.gfm import gfm
import html

katex_include = '''
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css" integrity="sha384-n8MVd4RsNIU0tAv4ct0nTaAbDJwPJzDEaqSD1odI+WdtXRGWt2kTvGFasHpSy3SV" crossorigin="anonymous">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js" integrity="sha384-XjKyOOlGwcjNTAIQHIpgOno0Hl1YQqzUOEleOLALmuqehneUG+vnGctmUb0ZY0l8" crossorigin="anonymous"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/contrib/auto-render.min.js" integrity="sha384-+VBxd3r6XgURycqtZ117nYw44OOcIax56Z4dCRWbxyPt0Koah1uHoK0o4+/RRE05" crossorigin="anonymous"></script>
<script>
    document.addEventListener("DOMContentLoaded", function () {
        renderMathInElement(document.body, {
            delimiters: [
                { left: '$$', right: '$$', display: true },
                { left: '$', right: '$', display: false },
                { left: '\(', right: '\)', display: false },
                { left: '\[', right: '\]', display: true },
                { left: "\begin{equation}", right: "\end{equation}", display: true },
                { left: "\begin{align}", right: "\end{align}", display: true },
            ],
            throwOnError: false
        });
    });
</script>   
'''

math_pattern = re.compile(r'(\$\$)(.*?)\$\$|(\$)(.*?)\$', re.DOTALL)


def md2seek(markdown, include_style=True):
    result = gfm.convert(markdown)
    if math_pattern.search(result):
        math_pattern.sub(
            lambda x: f"{(x.group(1) or x.group(3))}{html.unescape(x.group(2) or x.group(4))}{x.group(1) or x.group(3)}",
            result
        )
        result = katex_include + result
    if include_style:
        with files("seek_filler").joinpath("style.css").open("r") as f:
            result = f"<style>{f.read()}</style>\n" + result
    
    return result


def decomment(string):
    string = re.sub("#.*", "", string)
    string = re.sub("\n[\n]+", "\n\n", string, re.DOTALL)
    return string
