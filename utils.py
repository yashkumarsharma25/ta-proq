import re 
import bs4
import subprocess

def md2html(markdown):
    html = subprocess.run("pandoc --mathjax -f markdown-smart --standalone -M document-css=false",input=markdown,capture_output=True,text=True,shell=True).stdout
    soup = bs4.BeautifulSoup(html, 'html.parser')

    for elem in soup.find_all(["style","title", "meta"]):
        elem.extract()

    

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
    return result

def decomment(string):
    string = re.sub("#.*","",string)
    string = re.sub("\n[\n]+","\n\n",string,re.DOTALL)
    return string