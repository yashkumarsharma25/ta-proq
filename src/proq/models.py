import difflib
import json
import re
from importlib.resources import files
from typing import Annotated, Generic, TypeVar, Literal

from pydantic import (
    AliasChoices,
    BaseModel,
    BeforeValidator,
    Field,
    field_validator,
)

# curl https://emkc.org/api/v2/piston/runtimes | jq "sort_by(.language)| map({language: .language, aliases: .aliases})" > runtimes.json
# langs and aliases taken from piston
runtimes = json.loads(files("proq.data").joinpath("runtimes.json").read_text())
lang_code = {runtime["language"]: runtime["language"] for runtime in runtimes} | {
    alias: runtime["language"] for runtime in runtimes for alias in runtime["aliases"]
}
ProgLang = Annotated[
    Literal[
        "awk",
        "bash",
        "basic",
        "basic.net",
        "befunge93",
        "bqn",
        "brachylog",
        "brainfuck",
        "c",
        "c++",
        "cjam",
        "clojure",
        "cobol",
        "coffeescript",
        "cow",
        "crystal",
        "csharp",
        "csharp.net",
        "d",
        "dart",
        "dash",
        "dragon",
        "elixir",
        "emacs",
        "emojicode",
        "erlang",
        "file",
        "forte",
        "forth",
        "fortran",
        "freebasic",
        "fsharp.net",
        "fsi",
        "go",
        "golfscript",
        "groovy",
        "haskell",
        "husk",
        "iverilog",
        "japt",
        "java",
        "javascript",
        "javascript",
        "jelly",
        "julia",
        "kotlin",
        "lisp",
        "llvm_ir",
        "lolcode",
        "lua",
        "matl",
        "matl",
        "nasm",
        "nasm64",
        "nim",
        "ocaml",
        "octave",
        "osabie",
        "paradoc",
        "pascal",
        "perl",
        "php",
        "ponylang",
        "powershell",
        "prolog",
        "pure",
        "pyth",
        "python",
        "python2",
        "racket",
        "raku",
        "retina",
        "rockstar",
        "rscript",
        "ruby",
        "rust",
        "samarium",
        "scala",
        "smalltalk",
        "sqlite3",
        "swift",
        "typescript",
        "typescript",
        "vlang",
        "vyxal",
        "yeethon",
        "zig",
    ],
    BeforeValidator(lambda x: lang_code[x]),
]


class TestCase(BaseModel):
    input: str
    output: str


class ExecuteConfig(BaseModel):
    source_filename: str | None = ""
    build: str | None = ""
    run: str | None = ""


class Solution(BaseModel):
    prefix: str = Field(default="", description="The prefix of the solution")
    template: str = Field(
        default="", description="Template code between prefix and suffix"
    )
    solution: str = Field(
        default="", description="The solution code to replace template"
    )
    suffix: str = Field(default="", description="The suffix of the solution")
    suffix_invisible: str = Field(
        default="",
        validation_alias=AliasChoices("suffix_invisible", "invisible_suffix"),
        description="The invisible part of the suffix that comes after suffix",
    )
    lang: ProgLang = Field(default="python")
    execute_config: ExecuteConfig | None

    @property
    def solution_code(self):
        """The complete solution code with all prefix and suffix attached."""
        return "".join([self.prefix, self.solution, self.suffix, self.suffix_invisible])

    @property
    def template_code(self):
        """The complete template code with all prefix and suffix attached"""
        return "".join([self.prefix, self.template, self.suffix, self.suffix_invisible])

    @property
    def template_solution_diff(self):
        differ = difflib.Differ()
        differences = differ.compare(
            self.template.splitlines(keepends=True),
            self.solution.splitlines(keepends=True),
        )
        return list(differences)


class ProQ(BaseModel):
    """Pydantic model for a Programming Question (ProQ)"""

    title: str | None = Field(validation_alias="Title", description="Title")
    statement: str = Field(
        validation_alias="Problem Statement",
        description="The problem statement with example and explanation",
    )
    public_testcases: list[TestCase] = Field(validation_alias="Public Test Cases")
    private_testcases: list[TestCase] = Field(validation_alias="Private Test Cases")
    solution: Solution = Field(validation_alias="Solution", description="The solution")

    class Config:
        validate_assignment = True
        populate_by_name = True

    @field_validator("title")
    @classmethod
    def remove_duplicates(cls, word):
        """Removes multiple spaces and strips whitespace in beginning and end."""
        return re.sub(re.compile(r"\s+"), " ", word).strip()

    @classmethod
    def default_proq(cls):
        return cls(
            title="Sample Title",
            statement="Sample Problem statment",
            public_testcases=[TestCase(input="a", output="a")],
            private_testcases=[TestCase(input="a", output="a")],
            solution=Solution(
                solution="print(input())",
                lang="python",
            ),
        )


DataT = TypeVar("DataT")


class NestedContent(BaseModel, Generic[DataT]):
    title: str
    content: list["NestedContent[DataT]"] | DataT
