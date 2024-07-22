# Plan for: Refactoring Aider Coders and Prompts

## Objectives
- Separate edit formats from LLM entities
- Create a more flexible and modular structure
- Allow Coders to be used with specific objectives (Coding, Planning, Helping) and any editing format

## Tasks

1. [ ] Refactor base structure for Coders and Prompts
   - [ ] Create `aider/coders/edit_formats/base_format.py`
     - [ ] Define `BaseEditFormat` class for edit format operations
   - [ ] Update `aider/coders/base_coder.py`
     - [ ] Refine `BaseCoder` class with common functionality
   - [ ] Update `aider/coders/base_prompts.py`
     - [ ] Refine `BasePrompts` class with common prompt structures

2. [ ] Implement Edit Format classes
   - [ ] Create `aider/coders//edit_formats/unified_diff_format.py`
     - [ ] Implement `UnifiedDiffFormat` class extending `BaseEditFormat`
   - [ ] Create `aider/coders//edit_formats/editblock_format.py`
     - [ ] Implement `EditBlockFormat` class extending `BaseEditFormat`
   - [ ] Create `aider/coders//edit_formats/wholefile_format.py`
     - [ ] Implement `WholeFileFormat` class extending `BaseEditFormat`

3. [ ] Refactor existing Coder classes
   - [ ] Update `aider/coders/planner_coder.py`
     - [ ] Refactor `PlannerCoder` to use new structure
   - [ ] Update `aider/coders/developer_coder.py`
     - [ ] Refactor `DeveloperCoder` to use new structure
     - [ ] Move common "developer" skills from other coders into this class
   - [ ] Update `aider/coders/helper_coder.py`
     - [ ] Refactor `HelperCoder` to not use any diff format
   - [ ] Update `aider/coders/editblock_coder.py`
     - [ ] Refactor to use `EditBlockFormat`
   - [ ] Update `aider/coders/udiff_coder.py`
     - [ ] Refactor to use `UnifiedDiffFormat`
   - [ ] Update `aider/coders/wholefile_coder.py`
     - [ ] Refactor to use `WholeFileFormat`

4. [ ] Update Prompts classes
   - [ ] Update `aider/coders/planner_prompts.py`
   - [ ] Update `aider/coders/developer_prompts.py`
   - [ ] Update `aider/coders/helper_prompts.py`
   - [ ] Update `aider/coders/editblock_prompts.py`
   - [ ] Update `aider/coders/udiff_prompts.py`
   - [ ] Update `aider/coders/wholefile_prompts.py`

5. [ ] Implement CoderFactory for creating Coders with specific Edit Formats
   - [ ] Create `aider/coder_factory.py`
     - [ ] Implement `CoderFactory` class with methods to create Coders with specific Edit Formats

6. [ ] Update main application to use new Coder and Edit Format structure
   - [ ] Update `aider/main.py` to use the new `CoderFactory`

7. [ ] Write unit tests for new classes and structures
   - [ ] Create test files for each new and updated class

8. [ ] Update documentation
    - [ ] Update README.md with new structure and usage instructions
    - [ ] Update any existing documentation to reflect the new architecture

## Base code files involved
- aider/coders/base_coder.py: Will be updated with refined BaseCoder functionality
- aider/coders/base_prompts.py: Will be updated with refined BasePrompts functionality
- aider/edit_formats/base_format.py: New file for BaseEditFormat
- aider/edit_formats/unified_diff_format.py: New file for UnifiedDiffFormat
- aider/edit_formats/editblock_format.py: New file for EditBlockFormat
- aider/edit_formats/wholefile_format.py: New file for WholeFileFormat
- aider/coders/planner_coder.py: Will be refactored to use new structure
- aider/coders/developer_coder.py: Will be refactored to use new structure
- aider/coders/helper_coder.py: Will be refactored to not use any diff format
- aider/coders/editblock_coder.py: Will be refactored to use EditBlockFormat
- aider/coders/udiff_coder.py: Will be refactored to use UnifiedDiffFormat
- aider/coders/wholefile_coder.py: Will be refactored to use WholeFileFormat
- aider/coders/*_prompts.py: All prompt files will be updated
- aider/coder_factory.py: New file for CoderFactory
- aider/main.py: Will be updated to use CoderFactory

## Considerations and restrictions
- Maintain backwards compatibility where possible
- Ensure that the new structure allows for easy addition of new Coders and Edit Formats in the future
- Keep the core functionality of each Coder type (Developer, Planner, Helper) separate from the edit format logic
- HelpCoder should not use any diff format as it's not meant to create/edit files

## Next steps (Future considerations)
- Implement additional Coder types as needed (e.g., ReviewerCoder, OptimizationCoder)
- Explore the possibility of allowing users to define custom Prompts and Edit Formats
- Consider implementing a plugin system for easy extension of Coder and Edit Format capabilities

## Validation
- [ ] Plan validated by the user
- [ ] Implementation validated by the user

## Instructions for developers
- Always review the updated architecture documentation before starting work on any task.
- After completing a task, update this checklist by marking the task as complete.
- If any deviations or issues arise during task execution, communicate with the project lead for guidance.