from .base_format import BaseDiffFormat

class ReadonlyDiffFormat(BaseDiffFormat):
    id = "readonly"
    
    diff_format_instructions = "You can propose file edits in the chat but you can't make any edits directly."
    system_reminder = ""

    
    # attribute function
    @property
    def format_prompt(self):
        return f"*{self.name}*"

    def get_edits(self):
        raise []

    def apply_edits(self, edits):
        pass
    
    def format_file_diff(self, file_path, file_language, original_full=None, updated_full=None, chunks=None):
        return ""