import math
import re
from difflib import SequenceMatcher
from pathlib import Path

from .edit_formats.editblock_format import EditBlockDiffFormat

from .base_agent import Agent
from .planner_prompts import PlannerPrompts


class PlannerAgent(Agent):
    agent_type = "planner"

    def __init__(self, *args, diff_format=None, **kwargs):
        self.gpt_prompts = PlannerPrompts(diff_format=diff_format)
        super().__init__(*args, diff_format=diff_format, **kwargs)
        
    def get_files_messages(self):
        files_messages = []

        repo_content = self.get_repo_map()
        if repo_content:
            files_messages += [
                dict(role="user", content=repo_content),
                dict(
                    role="assistant",
                    content="Ok, If `PROJECT_OVERVIEW.md` & `CURRENT_PLAN.md` are listed in the repository I'm going to add you to read their content and any other file I found relevant understand the overall project. If files are not present in your repository, I will create them after collecting feedback from you about your requirements.",
                ),
            ]

        if self.abs_fnames:
            files_content = self.gpt_prompts.files_content_prefix
            files_content += self.get_files_content()
            files_reply = "Ok, any changes I propose will be to those files."
        elif repo_content:
            files_content = self.gpt_prompts.files_no_full_files_with_repo_map
            files_reply = self.gpt_prompts.files_no_full_files_with_repo_map_reply
        else:
            files_content = self.gpt_prompts.files_no_full_files
            files_reply = "Ok."

        if files_content:
            files_messages += [
                dict(role="user", content=files_content),
                dict(role="assistant", content=files_reply),
            ]

        images_message = self.get_images_message()
        if images_message is not None:
            files_messages += [
                images_message,
                dict(role="assistant", content="Ok."),
            ]

        return files_messages