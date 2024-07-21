from .parse import proq_to_json
import sys 
import subprocess

def get_source_code(code:dict):
    return code["prefix"]+code["solution"]+code["suffix"]+code["suffix_invisible"]

def get_template(code:dict):
    return code["prefix"]+code["template"]+code["suffix"]+code["suffix_invisible"]


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


def check_testcases(run_command, testcases, verbose=True):
    status = []
    for i,testcase in enumerate(testcases,1):
        stdin = testcase['input']
        expected_output = testcase['output']
        actual_output = run_script(run_command, stdin)
        
        if actual_output.strip() == expected_output.strip():
            status.append(True)
            if verbose:
                print(f"Test case {i} passed")
        else:
            status.append(False)
            if verbose:
                print(f"Test case {i} failed.",
                    "Input:",
                    stdin,
                    "Expected output:", 
                    expected_output, 
                    "Actual output:", 
                    actual_output,
                    sep="\n"
                )
    return status

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

        ok_message = "\033[0;32mOK\033[0m"
        with open(script_file_name, "w") as f:
            f.write(get_template(problem["code"]))
        try:
            if build_command:
                build(build_command)
        except BuildFailedException:
            print(f"Build Failed for {problem['title']}")
            template_check_status = ok_message

        template_public_testcases = check_testcases(run_command,problem["testcases"]["public_testcases"],verbose=False)
        template_private_testcases = check_testcases(run_command,problem["testcases"]["public_testcases"],verbose=False)
        if not any(template_public_testcases+template_private_testcases):
            template_check_status = ok_message
        else:
            true_indices = lambda items: map(lambda x:x[0], filter(lambda x: x[1], enumerate(items,1)))
            template_check_status = f"\033[0;31mFailed\nPublic Testcases : {','.join(map(str,true_indices(template_public_testcases)))} Passed"
            template_check_status += f"\nPrivate Testcases : {','.join(map(str,true_indices(template_private_testcases)))} Passed\033[0m"
        print(f"Template Check Status({problem['title']}):",template_check_status)
        
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
    