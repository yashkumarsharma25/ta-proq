import re 
import bs4
import subprocess
from importlib.resources import files
from marko.ext.gfm import gfm

def md2seek(markdown, include_style=True):
    result = gfm.convert(markdown)
    if include_style:
        with files("seek_filler").joinpath("style.css").open("r") as f:
            result = f"<style>{f.read()}</style>\n" + result
    return result

def decomment(string):
    string = re.sub("#.*","",string)
    string = re.sub("\n[\n]+","\n\n",string,re.DOTALL)
    return string