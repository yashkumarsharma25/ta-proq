import argparse
from . import ProqFiller


def create_proqs(
    course_code, proq_file, domain="onlinedegree", use_existing_unit=False
):
    filler = ProqFiller()
    filler.open_url(
        f"https://backend.seek.{domain}.iitm.ac.in/modules/firebase_auth/login?continue=https://backend.seek.{domain}.iitm.ac.in/{course_code}/dashboard"
    )
    filler.load_data(proq_file)
    filler.create_proqs(create_unit=not new_unit)


def main():
    parser = argparse.ArgumentParser(description="Generate a template for problems")
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
        action="store_false",
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
    args = parser.parse_args()
    if not args.course_code:
        args.course_code = input("Enter course code: ")
    if not args.proq_file:
        args.proq_file = input("Enter problems file name: ")

    create_proqs(**vars(args))


if __name__ == "__main__":
    main()
