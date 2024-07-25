from pathlib import Path

from .planner_agent import PlannerAgent
from .developer_prompts import DeveloperPrompts


class DeveloperAgent(PlannerAgent):
    agent_type = "developer"

    def __init__(self, *args, diff_format=None, plan_file=None, overview_file=None, **kwargs):
        
        super().__init__(*args, diff_format=diff_format, plan_file=plan_file, overview_file=overview_file, **kwargs)
        self.gpt_prompts = DeveloperPrompts(
            diff_format=diff_format, 
            overview_file=self.overview_file,
            plan_file=self.plan_file, 
            plan_file_exists=self.plan_file_exists, 
            overview_file_exists=self.overview_file_exists)
    
    def pre_run_setup(self):
        super().pre_run_setup()
        # add dependencies for the developer agent by default
        if self.plan_file and self.plan_file_exists:
            self.add_rel_fname(self.plan_file)
        if self.overview_file and self.overview_file_exists:
            self.add_rel_fname(self.overview_file)
