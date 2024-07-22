from .base_agent import Agent
from .help_prompts import HelpPrompts


class HelpAgent(Agent):
    edit_format = "help"

    def __init__(self, *args, **kwargs):
        self.gpt_prompts = HelpPrompts()
        super().__init__(*args, **kwargs)
