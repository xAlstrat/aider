from aider import diffs
from pathlib import Path

from .base_format import BaseDiffFormat
from ...dump import dump  # noqa: F401

class WholeDiffFormat(BaseDiffFormat):
    id = "whole"
    
    diff_format_instructions = """Once you understand the request you MUST:
1. Determine if any code changes are needed.
2. Explain any needed changes.
3. If changes are needed, output a copy of each file that needs changes."""
    
    
    def format_file_diff(self, file_path, file_language, original_full=None, updated_full=None, chunks=None):
        updated_full = updated_full + "\n" if updated_full else ""
        return  f"""{file_path}
{{fence[0]}}
{updated_full}{{fence[1]}}"""

    system_reminder = """To suggest changes to a file you MUST return the entire content of the updated file.
You MUST use this *file listing* format:

path/to/filename.js
{fence[0]}
// entire file content ...
// ... goes in between
{fence[1]}

Every *file listing* MUST use this format:
- First line: the filename with any originally provided path
- Second line: opening {fence[0]}
- ... entire content of the file ...
- Final line: closing {fence[1]}

To suggest changes to a file you MUST return a *file listing* that contains the entire content of the file.
*NEVER* skip, omit or elide content from a *file listing* using "..." or by adding comments like "... rest of code..."!
Create a new file you MUST return a *file listing* which includes an appropriate filename, including any appropriate path.

{lazy_prompt}
"""

    def get_edits(self, mode="update"):
        content = self.agent.get_multi_response_content()

        chat_files = self.agent.get_inchat_relative_files()

        output = []
        lines = content.splitlines(keepends=True)

        edits = []

        saw_fname = None
        fname = None
        fname_source = None
        new_lines = []
        for i, line in enumerate(lines):
            if line.startswith(self.agent.fence[0]) or line.startswith(self.agent.fence[1]):
                if fname is not None:
                    # ending an existing block
                    saw_fname = None

                    full_path = self.agent.abs_root_path(fname)

                    if mode == "diff":
                        output += self.do_live_diff(full_path, new_lines, True)
                    else:
                        edits.append((fname, fname_source, new_lines))

                    fname = None
                    fname_source = None
                    new_lines = []
                    continue

                # fname==None ... starting a new block
                if i > 0:
                    fname_source = "block"
                    fname = lines[i - 1].strip()
                    fname = fname.strip("*")  # handle **filename.py**
                    fname = fname.rstrip(":")
                    fname = fname.strip("`")

                    # Did gpt prepend a bogus dir? It especially likes to
                    # include the path/to prefix from the one-shot example in
                    # the prompt.
                    if fname and fname not in chat_files and Path(fname).name in chat_files:
                        fname = Path(fname).name
                if not fname:  # blank line? or ``` was on first line i==0
                    if saw_fname:
                        fname = saw_fname
                        fname_source = "saw"
                    elif len(chat_files) == 1:
                        fname = chat_files[0]
                        fname_source = "chat"
                    else:
                        # TODO: sense which file it is by diff size
                        raise ValueError(
                            f"No filename provided before {self.agent.fence[0]} in file listing"
                        )

            elif fname is not None:
                new_lines.append(line)
            else:
                for word in line.strip().split():
                    word = word.rstrip(".:,;!")
                    for chat_file in chat_files:
                        quoted_chat_file = f"`{chat_file}`"
                        if word == quoted_chat_file:
                            saw_fname = chat_file

                output.append(line)

        if mode == "diff":
            if fname is not None:
                # ending an existing block
                full_path = (Path(self.agent.root) / fname).absolute()
                output += self.do_live_diff(full_path, new_lines, False)
            return "\n".join(output)

        if fname:
            edits.append((fname, fname_source, new_lines))

        seen = set()
        refined_edits = []
        # process from most reliable filename, to least reliable
        for source in ("block", "saw", "chat"):
            for fname, fname_source, new_lines in edits:
                if fname_source != source:
                    continue
                # if a higher priority source already edited the file, skip
                if fname in seen:
                    continue

                seen.add(fname)
                refined_edits.append((fname, fname_source, new_lines))

        return refined_edits

    def apply_edits(self, edits):
        for path, fname_source, new_lines in edits:
            full_path = self.agent.abs_root_path(path)
            new_lines = "".join(new_lines)
            self.agent.io.write_text(full_path, new_lines)

    def do_live_diff(self, full_path, new_lines, final):
        if Path(full_path).exists():
            orig_lines = self.agent.io.read_text(full_path).splitlines(keepends=True)

            show_diff = diffs.diff_partial_update(
                orig_lines,
                new_lines,
                final=final,
            ).splitlines()
            output = show_diff
        else:
            output = ["```"] + new_lines + ["```"]

        return output
