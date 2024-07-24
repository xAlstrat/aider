from pathlib import Path

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
            
    def get_system_reminder(self):
        return f"""
# AI Assistant Rules Reminder:
    - Your *ONLY* objective is to *development a plan* at `{self.plan_file}` file based on the user's requirements.
    - *Always* ask question to the user to understand it more deeply.
    {"- *Always* check the current plan status and validate with the user to update or discard it before start working on a new plan." if self.plan_file_exists else ""}
    - {"Keep overview file as updated as possible." if self.overview_file_exists else f"Collect as many details as possible to create `{self.overview_file}` file."}
    - You must *ONLY* read/create/update files if that helps you *designing* the plan.
    - *Do not write code* or solve tasks related to the plan. Just do planning, that's your role.
    - Keep asking questions to the user as new context is given until is enough to write a complete plan.

    * `{self.overview_file}` Considerations:*
    - Keep only *current* system details, features, considerations, restrictions, challenges, key files descriptions, etc
    - Add relevant information that transcends the plan
    - * Do not * add capabilities or features that are not implemented yet or are still in development

{self.diff_format.system_reminder}
    """

    def get_files_messages(self):
        files_messages = []

        repo_content = self.get_repo_map()
        if repo_content:
            files_messages += [
                dict(role="user", content=repo_content),
                dict(
                    role="assistant",
                    content="Ok, I won't try to edit those files. I'll only use those files for planning",
                ),
            ]

        if self.abs_fnames:
            files_content = self.gpt_prompts.files_content_prefix
            files_content += self.get_files_content()
            files_reply = self.gpt_prompts.files_content_reply
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