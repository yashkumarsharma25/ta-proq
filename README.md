# Backend Filler

This project is started as `backend_filler` to be used to upload programming questions with seek backend. 

Then also added some functions to support testcase filling in replit.


## Top level modules

- **web_fillers** - contains generic form fillers for the web
  - `filler.py` - contains generic filler functions
  - `replit_filler.py` - contains functions to fill replit testcases.
- **seek_filler** - contains command-line tools and functions to author, test, and configure to the seek backend using selenium script.

### Command-line tools in `seek_filler` module
Use `command --help` to know how to use the below tools
- `proq-template` - a fully featured commandline tool to create a markdown template for configuring the programming questions. Use `proq-template --help` for more info.
- `proq2json` - a commandline utility for dumping `proq` files (md files) to json.
- `proq-evaluate` - for evaluating the testcases.
- `proq-upload` - interactive cli to upload the proqs to the seek backend.