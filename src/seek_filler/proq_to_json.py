from markdown_to_json import dictify
import yaml
import json
import re

def extract_solution(solution):
    code = {}
    
    code_parts = ["prefix","suffix","suffix_invisible","solution","template"]
    for part in code_parts:
        code[part] = re.findall(f"<{part}>(.*)</{part}>",solution,re.MULTILINE|re.DOTALL )
        code[part] = code[part][0].strip("\n") if code[part] else ""
            
    code["template"] = re.sub("<solution>(.*)</solution>","",code["template"],flags=re.MULTILINE|re.DOTALL )
    print(code["template"])
    return code

def extract_testcases(testcases_dict):
    testcases_list = list(testcases_dict.values())
    testcases = []
    for input, output in zip(testcases_list[::2],testcases_list[1::2]):
        testcases.append({
            "input":input.strip("\n").replace("```","").lstrip("\n"),
            "output":output.strip("\n").replace("```","").lstrip("\n")
        })
    return testcases

def proq_to_json(proq_file, to_file=False):
    with open(proq_file) as f:
        raw_content = f.read()
        _,yaml_header , markdown = raw_content.split("---",2)
        markdown_content = dictify(markdown)
        yaml_header = yaml.safe_load(yaml_header)
    unit_name, problems = markdown_content.popitem()
    problem_names = list(problems.keys())
    print(problem_names)
    for problem_name in problem_names:
        problem = problems[problem_name]
        problem["title"] = problem_name
        problem["statement"] = problem.pop("Problem Statement")
        problem["code"] = extract_solution(problem.pop("Solution"))
        problem["testcases"] =problem.pop("Testcases")
        problem["testcases"]["public_testcases"] = extract_testcases(problem["testcases"].pop("Public Testcases"))
        problem["testcases"]["private_testcases"] = extract_testcases(problem["testcases"].pop("Private Testcases"))
        problem.update(yaml_header)
    problems = list(problems.values())
    if to_file:
        with open(f"{unit_name}.json","w") as f:
            json.dump(problems,f,indent=2)
    return unit_name, problems

import sys
import os

if __name__ == "__main__":
    files = sys.argv[1:]
    for f in files:
        try:
            assert os.path.isfile(f), f"{f} is not a valid file"
            proq_to_json(f)
        except AssertionError as e:
            print(e)