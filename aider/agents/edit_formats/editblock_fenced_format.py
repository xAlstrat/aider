from . import EditBlockDiffFormat

class EditBlockFencedDiffFormat(EditBlockDiffFormat):
    id = "edit_block_fenced"
    
    def format_file_diff(self, file_path, file_language, original_full=None, updated_full=None, chunks=None):
        # no need to use original_full and updated_full for this format
        formatted_chunks = []
        
        for chunk_original, chunk_updated in chunks:
            original = chunk_original + "\n" if chunk_original else ""
            updated = chunk_updated + "\n" if chunk_updated else ""
            
            formatted_chunk = f"""{{fence[0]}}
{file_path}
<<<<<<< SEARCH
{original}=======
{updated}>>>>>>> REPLACE
{{fence[1]}}"""
        
            formatted_chunks.append(formatted_chunk)
        
        return "\n\n".join(formatted_chunks)