import argparse
from . import proq_gen
from . import proq_evaluate
from . import proq_to_json
from . import proq_upload



def main():
    # Create the main parser
    parser = argparse.ArgumentParser(prog='proq', description='Process some queries.')

    # Create the subparsers
    subparsers = parser.add_subparsers(title='subcommands', description='valid subcommands', help='additional help', dest='command')

    parser_template = subparsers.add_parser('template', help='Generate proq templates with given configuration')
    proq_gen.configure_cli_parser(parser_template)

    parser_evaluate = subparsers.add_parser('evaluate', help='Evaluate the testcases locally')
    proq_evaluate.configure_cli_parser(parser_evaluate)

    parser_export = subparsers.add_parser('export', help='Export to JSON or HTML')
    proq_to_json.conifgure_cli_parser(parser_export)

    parser_upload = subparsers.add_parser('upload', help='Upload proq using selenium using chrome')
    proq_upload.configure_cli_parser(parser_upload)

    # Parse the arguments

    args = parser.parse_args()
    if args.command:
        args.func(args)
    else:
        parser.print_help()
    