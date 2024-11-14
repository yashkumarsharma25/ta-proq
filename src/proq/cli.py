import argparse

from termcolor import colored

from . import create, evaluate, export


def main():
    # Create the main parser
    parser = argparse.ArgumentParser(
        prog="proq",
        description="A Command-line suite for authoring Programming Questions",
    )

    # Create the subparsers
    subparsers = parser.add_subparsers(
        title=colored("Commands", attrs=["bold"]), dest="command", metavar="COMMAND"
    )

    parser_template = subparsers.add_parser(
        "create", help="Generate proq templates with given configuration"
    )
    create.configure_cli_parser(parser_template)

    parser_evaluate = subparsers.add_parser(
        "evaluate", help="Evaluate the testcases locally"
    )
    evaluate.configure_cli_parser(parser_evaluate)

    parser_export = subparsers.add_parser("export", help="Export to JSON,HTML or PDF")
    export.conifgure_cli_parser(parser_export)

    # Parse the arguments

    args = parser.parse_args()
    if args.command:
        args.func(args)
    else:
        parser.print_help()
