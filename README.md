# Proq

Proq - A commandline tool for authoring programming questions at scale.


This project is started as `backend_filler` to be used to upload programming questions with seek backend. 

Then also added some functions to support testcase filling in replit.

Now it was made as a stand alone tool for authoring programming questions and evaluating them.

## The proq commandline

- **`proq`** - The main commandline tool with subcommands for creating, evaluating, exporting and publishing programming questions.

### Subcommands
Use `proq subcommand --help` to know more about the subcommand.

- `proq create` - create a markdown template for authoring the programming questions.
- `proq evaluate` - evaluate the testcases configured using the build and compile process defined with the yaml header.
- `proq export` - export the parsed markdown as JSON or html
- `proq upload` - upload the proq to seek.

