import re 
import bs4
import subprocess
from importlib.resources import open_text

def md2html(markdown, include_style=True):
    html = subprocess.run("pandoc --mathjax -f markdown-smart -M document-css=false",input=markdown,capture_output=True,text=True,shell=True).stdout
    soup = bs4.BeautifulSoup(html, 'html.parser')

    code_elements = soup.find_all('code', recursive=True)
    filtered_code_elements = [element for element in code_elements if element.find_parent('pre') is None]
    
    for element in filtered_code_elements:
        new_tag = soup.new_tag('span')
        new_tag['style'] = 'color:red;font-family:monospace'
        new_tag.string = element.text
        element.replace_with(new_tag)
    soup_str = str(soup.find("head")) + str(soup.find("body"))
    

    result=re.sub(r'<!--.*?-->','', soup_str,re.DOTALL)
    result = re.sub(r"\n+","\n",result)
    math_mapping = {
        r"\\\[":"<p><gcb-math>",
        r"\\\]":"</gcb-math></p>",
        r"\\\(":"<gcb-math>",
        r"\\\)":"</gcb-math>",
    }
    for pat, replace in math_mapping.items():
        result = re.sub(pat,replace,result)
    if include_style:
        with open_text("style.css") as f:
            result = f"<style>{f.read()}</style>\n" + result
    return result

def decomment(string):
    string = re.sub("#.*","",string)
    string = re.sub("\n[\n]+","\n\n",string,re.DOTALL)
    return string