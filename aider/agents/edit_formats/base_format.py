class BaseDiffFormat:

    diff_format_instructions = None
    system_reminder = None
    agent = None
    
    def get_edits(self):
        # raise not implemented
        raise NotImplementedError()

    def apply_edits(self, edits):
        # raise not implemented
        raise NotImplementedError()
    
    def format_file_diff(self, file_path, file_language, original_full=None, updated_full=None, chunks=None):
        # raise not implemented
        raise NotImplementedError()
