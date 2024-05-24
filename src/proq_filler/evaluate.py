from .export import proq_to_json
import sys 
import subprocess

def get_source_code(code:dict):
    return code["prefix"]+code["solution"]+code["suffix"]+code["suffix_invisible"]


class BuildFailedException(Exception):
    pass

def build(build_command):
    build_process = subprocess.run(
        build_command.split(" "), 
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE
    )
    if build_process.returncode == 0:
        print("Compilation successful.")
    else:
        raise BuildFailedException


def run_script(run_command, stdin):
    run_process = subprocess.run(
        run_command.split(" "), 
        input=stdin.encode('utf-8'), 
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE
    )
    
    if run_process.returncode == 0:
        return run_process.stdout.decode('utf-8')
    else:
        return run_process.stdout.decode('utf-8') + run_process.stderr.decode('utf-8')


def check_testcases(run_command, testcases):
    for i,testcase in enumerate(testcases,1):
            stdin = testcase['input']
            expected_output = testcase['output']
            actual_output = run_script(run_command, stdin)
            
            if actual_output.strip() == expected_output.strip():
                print(f"Test case {i} passed")
            else:
                print(f"Test case {i} failed.",
                    "Expected output:", 
                    expected_output, 
                    "Actual output:", 
                    actual_output,
                    sep="\n"
                )

def evaluate_proq(proq_file):
    _, problems = proq_to_json(proq_file)

    for problem in problems:
        script_file_name = problem["local_evaluate"]["source_file"]
        build_command = problem["local_evaluate"].get("build", None)
        run_command = problem["local_evaluate"]["run"]

        # write source code to file
        print(problem["title"])
        with open(script_file_name, "w") as f:
            f.write(get_source_code(problem["code"]))

        try:
            if build_command:
                build(build_command)
        except BuildFailedException:
            print(f"Build Failed for {problem['title']}")
            continue

        print("Public Testcases")
        check_testcases(run_command,problem["testcases"]["public_testcases"])
        print("Private Testcases")
        check_testcases(run_command,problem["testcases"]["private_testcases"])
        print()

import os
import argparse 

def evaluate_proqs(files):
    for file_path in files:
        if not os.path.isfile(file_path):
            print(f"{file_path} is not a valid file")
            continue
        print(f"Evaluating file {file_path}")
        evaluate_proq(file_path)

def configure_cli_parser(parser:argparse.ArgumentParser):
    parser.add_argument("files", metavar="F", type=str, nargs="+", help="proq files to be evaluated")
    parser.set_defaults(func = lambda args: evaluate_proqs(args.files))
    