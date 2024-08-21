import argparse
import asyncio
from .filler.seek_filler import SeekFiller
    
def configure_cli_parser(parser:argparse.ArgumentParser):
    parser.add_argument(
        "proq_file", metavar="PROQ_FILE", type=str, help="The Proq file"
    )
    parser.add_argument("proq_nums", metavar="PROQ_NUMS", type=str, nargs="*", help="The proq numbers to update only the selected proqs from the file")
    parser.add_argument(
        "--show-browser",
        action="store_true",
        help="Open the browser while filling. Default will be headless mode.",
        required=False,
    )

    parser.add_argument("--course-code", type=str, help="Course code as 24t1_cs1002", required=False)
    parser.add_argument(
        "--profile", type=str, help="Name of the Profile directory", required=False
    )
    parser.add_argument(
        "--login-id", type=str, help="Email ID for login to Chrome", required=False
    )
    parser.add_argument(
        "--domain",
        type=str,
        default="seek.onlinedegree",
        help="Domain in the URL",
        required=False,
    )
    parser.set_defaults(
        func = lambda args: asyncio.run(SeekFiller().upload_proqs(
            proq_file = args.proq_file,
            course_code = args.course_code,
            headless= not args.show_browser,
            proq_nums = args.proq_nums,
            domain= args.domain,
            profile = args.profile,
            login_id = args.login_id
        ))
    )
    
    