from .parse import load_proq, ProqSet
import sys 
import subprocess
from collections import namedtuple

ProqChecks = namedtuple("ProqChecks",["solution_checks","template_checks"])

def get_source_code(code:dict):
    return code["prefix"]+code["solution"]+code["suffix"]+code["suffix_invisible"]

def get_template(code:dict):
    return code["prefix"]+code["template"]+code["suffix"]+code["suffix_invisible"]


def write_to_file(content, file_name):
    with open(file_name, "w") as f:
        f.write(content)

def build(build_command) -> bool:
    '''
    Builds with the given build command.

    Args:
        build_command : str - build command to run in a subprocess

    Return:
        bool - Return code from the build process
    '''
    build_process = subprocess.run(
        build_command.split(" "), 
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE
    )
    return build_process.returncode==0


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


def check_testcases(run_command, testcases, verbose=False):
    status = []
    for i,testcase in enumerate(testcases,1):
        stdin = testcase['input']
        expected_output = testcase['output']
        actual_output = run_script(run_command, stdin)
        
        if actual_output.strip().replace("\r","") == expected_output.strip():
            status.append(True)
            if verbose:
                print(f"\033[0;32mTest case {i} passed\033[0m")
        else:
            status.append(False)
            if verbose:
                print(f"\033[0;31mTest case {i} failed.")
                if stdin.strip():
                    print("Input:",stdin,sep="\n")
                print(
                    "Expected output:", 
                    expected_output, 
                    "Actual output:", 
                    actual_output,
                    "\033[0m",
                    sep="\n"
                )
    return status

def evaluate_proq(proqs,verbose=False)->dict[str,ProqChecks]:
    proq_checks = {}
    for problem in proqs:
        script_file_name = problem["local_evaluate"]["source_file"]
        build_command = problem["local_evaluate"].get("build", None)
        run_command = problem["local_evaluate"]["run"]
        public_testcases  = problem["testcases"]["public_testcases"]
        private_testcases  = problem["testcases"]["private_testcases"]
        # write source code to file
        if verbose:
            print(problem["title"])
        
        # write solution
        write_to_file(get_source_code(problem["code"]),script_file_name)

        # build source
        if build_command:
            build_passed = build(build_command) 
            if not build_passed:
                if verbose:
                    print(f"\033[0;31mBuild Failed\033[0m")
                proq_checks[problem['title']] = ProqChecks(
                    solution_checks=False,
                    template_checks=False
                )
                continue
        
        # check testcases with source
        if verbose:
            print("\033[0;1mPublic Testcases\033[0m")
        solution_public_testcases = check_testcases(run_command,public_testcases, verbose=verbose)
        if verbose:
            print("\033[0;1mPrivate Testcases\033[0m")
        solution_private_testcases = check_testcases(run_command,private_testcases, verbose=verbose)
        solution_passed = all(solution_public_testcases+solution_private_testcases)
        if not solution_passed:
            proq_checks[problem['title']] = ProqChecks(
                solution_checks=False,
                template_checks=False
            )
            continue

        # Template check

        # write solution
        write_to_file(get_template(problem["code"]),script_file_name)

        build_passed = True
        if build_command:
            build_passed = build(build_command)
        
        if build_passed:
            template_public_testcases = check_testcases(run_command,public_testcases,verbose=False)
            template_private_testcases = check_testcases(run_command,private_testcases,verbose=False)
        
        any_template_passed = build_passed and any(
            template_public_testcases+template_private_testcases
        )

        proq_checks[problem['title']] = ProqChecks(
            solution_checks=True,
            template_checks=not any_template_passed
        )

        if verbose:
            print(f"\033[0;1mTemplate Check:\033[0m ",end="")
            if proq_checks[problem['title']].template_checks:
                print("\033[0;32mPassed\033[0m")
            else:
                true_indices = lambda items: map(lambda x:x[0], filter(lambda x: x[1], enumerate(items,1)))
                print(f"\033[0;31mFailed\nPublic Testcases : {','.join(map(str,true_indices(template_public_testcases)))} Passed")
                print(f"Private Testcases : {','.join(map(str,true_indices(template_private_testcases)))} Passed\033[0m")
            print()
        
    return proq_checks
    
import os
import argparse 

def evaluate_proqs(files):
    for file_path in files:
        if not os.path.isfile(file_path):
            print(f"{file_path} is not a valid file")
            continue
        print(f"Evaluating file {file_path}")
        evaluate_proq(load_proq(file_path).proqs,verbose=True)

def configure_cli_parser(parser:argparse.ArgumentParser):
    parser.add_argument("files", metavar="F", type=str, nargs="+", help="proq files to be evaluated")
    parser.set_defaults(func = lambda args: evaluate_proqs(args.files))
    