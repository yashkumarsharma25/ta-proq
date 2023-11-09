import json
from web_fillers import ReplitFiller

filler = ReplitFiller(profile_directory="Default")
page = "https://replit.com/@sep-dec-2023-python-remedial"
repl = "Find-substrings"

with open(f"testcases/{repl}.json") as testcases:
    testcases = json.load(testcases)
    filler.driver.get(f"{page}/{repl}")    
    filler.fill_testcases(testcases)