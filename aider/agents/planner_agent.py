import math
import re
from difflib import SequenceMatcher
from pathlib import Path

from .edit_formats.editblock_format import EditBlockDiffFormat

from .base_agent import Agent
from .planner_prompts import PlannerPrompts


class PlannerAgent(Agent):
    agent_type = "planner"
    

    def __init__(self, *args, diff_format=None, plan_file=None, overview_file=None, **kwargs):
        self.plan_file=plan_file
        self.overview_file=overview_file
        self.plan_file_exists = Path(self.plan_file).exists()
        self.overview_file_exists = Path(self.overview_file).exists()
        
        self.gpt_prompts = PlannerPrompts(
            diff_format=diff_format, 
            overview_file=self.overview_file,
            plan_file=self.plan_file, 
            plan_file_exists=self.plan_file_exists, 
            overview_file_exists=self.overview_file_exists)
        super().__init__(*args, diff_format=diff_format, **kwargs)
        
    def pre_run_setup(self):
        # add dependencies for the planner agent by default
        
        if self.plan_file and self.plan_file_exists:
            self.add_rel_fname(self.plan_file)
        if self.overview_file and self.overview_file_exists:
            self.add_rel_fname(self.overview_file)

    def get_files_messages(self):
        files_messages = []

        repo_content = self.get_repo_map()
        # if repo_content:
        files_messages += [
            dict(role="user", content=repo_content or "Tell me what your role is"),
            dict(
                role="assistant",
                content=f"""Ok, I will try to understand your system and requirements the best as possible to generate the best possible plan keeping the overview up to date.
{f"Also, a plan already exists at {self.plan_file}, my job is to check its status and *validate* with you before start working in a new plan" if self.plan_file_exists else "I understand my main objective is to create a plan"}
                """,
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