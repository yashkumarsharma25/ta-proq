import argparse
import asyncio
from .filler.seek_filler import SeekFiller


async def upload_proqs(
    course_code, proq_file, domain="onlinedegree", use_existing_unit=False, profile=None, login_id=None
):
    filler = SeekFiller()
    await filler.init(login_id,profile)
    filler.load_data(proq_file)
    await filler.goto_course_dashboard("24t1_cs1002")
    filler.page.goto(
        f"https://backend.seek.{domain}.iitm.ac.in/modules/firebase_auth/login?continue=https://backend.seek.{domain}.iitm.ac.in/{course_code}/dashboard"
    )
    filler.load_data(proq_file)
    await filler.create_proqs(create_unit=not use_existing_unit)

def upload_proqs_interactive(
    course_code=None, proq_file=None, domain="onlinedegree", use_existing_unit=False, profile=None, login_id=None
):
    if not course_code:
        course_code = input("Enter course code: ")
    if not proq_file:
        proq_file = input("Enter problems file name: ")

    asyncio.run(upload_proqs(course_code, proq_file, domain, use_existing_unit, profile, login_id))
    
def configure_cli_parser(parser:argparse.ArgumentParser):
    parser.add_argument(
        "--profile", type=str, help="Name of the Profile directory", required=False
    )
    parser.add_argument(
        "--login-id", type=str, help="Email ID for login to Chrome", required=False
    )
    parser.add_argument("--course-code", type=str, help="Course code", required=False)
    parser.add_argument(
        "--proq-file", type=str, help="Problems file name", required=False
    )
    parser.add_argument(
        "--use-existing-unit",
        action="store_true",
        help="Optional flag to use an existing unit",
        required=False,
    )
    parser.add_argument(
        "--domain",
        type=str,
        choices=["nptel", "onlinedegree"],
        default="onlinedegree",
        help="Domain (nptel or onlinedegree)",
        required=False,
    )
    parser.set_defaults(
        func = lambda args: upload_proqs_interactive(
            args.course_code, 
            args.proq_file, 
            args.domain, 
            args.use_existing_unit, 
            args.profile, 
            args.login_id
        )
    )
    