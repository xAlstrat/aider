# Plan for: Refactoring Aider Coders and Prompts

## Objectives
- Separate edit formats from LLM entities
- Create a more flexible and modular structure
- Allow Coders to be used with specific objectives (Coding, Planning, Helping) and any editing format

## Tasks

1. [ ] Create a new base structure for Coders and Prompts
   - [ ] Create `aider/coders/base_coder.py`
     - [ ] Define `BaseCoder` class with common functionality
   - [ ] Create `aider/coders/base_prompts.py`
     - [ ] Define `BasePrompts` class with common prompt structures
   - [ ] Create `aider/edit_formats/base_format.py`
     - [ ] Define `BaseEditFormat` class for edit format operations

2. [ ] Implement new Coder classes
   - [ ] Create `aider/coders/developer_coder.py`
     - [ ] Implement `DeveloperCoder` class
   - [ ] Create `aider/coders/planner_coder.py`
     - [ ] Implement `PlannerCoder` class
   - [ ] Create `aider/coders/helper_coder.py`
     - [ ] Implement `HelperCoder` class

3. [ ] Implement new Prompts classes
   - [ ] Create `aider/prompts/developer_prompts.py`
     - [ ] Implement `DeveloperPrompts` class
   - [ ] Create `aider/prompts/planner_prompts.py`
     - [ ] Implement `PlannerPrompts` class
   - [ ] Create `aider/prompts/helper_prompts.py`
     - [ ] Implement `HelperPrompts` class

4. [ ] Implement Edit Format classes
   - [ ] Create `aider/edit_formats/udiff_format.py`
     - [ ] Implement `UDiffFormat` class
   - [ ] Create `aider/edit_formats/editblock_format.py`
     - [ ] Implement `EditBlockFormat` class
   - [ ] Create `aider/edit_formats/wholefile_format.py`
     - [ ] Implement `WholeFileFormat` class

5. [ ] Update existing Coder classes to use new structure
   - [ ] Update `aider/coders/editblock_coder.py`
   - [ ] Update `aider/coders/udiff_coder.py`
   - [ ] Update `aider/coders/help_coder.py`

6. [ ] Update existing Prompts classes to use new structure
   - [ ] Update `aider/coders/editblock_prompts.py`
   - [ ] Update `aider/coders/udiff_prompts.py`
   - [ ] Update `aider/coders/help_prompts.py`

7. [ ] Implement factory method for creating Coders with specific Edit Formats
   - [ ] Create `aider/coder_factory.py`
     - [ ] Implement `CoderFactory` class with methods to create Coders with specific Edit Formats

8. [ ] Update main application to use new Coder and Edit Format structure
   - [ ] Update `aider/main.py` to use the new `CoderFactory`

9. [ ] Write unit tests for new classes and structures
   - [ ] Create test files for each new and updated class

10. [ ] Update documentation
    - [ ] Update README.md with new structure and usage instructions
    - [ ] Update any existing documentation to reflect the new architecture

## Base code files involved
- aider/coders/base_coder.py: Will be refactored to contain only base Coder functionality
- aider/coders/base_prompts.py: Will be refactored to contain only base Prompts functionality
- aider/coders/editblock_coder.py: Will be updated to use new structure
- aider/coders/udiff_coder.py: Will be updated to use new structure
- aider/coders/help_coder.py: Will be updated to use new structure
- aider/coders/editblock_prompts.py: Will be updated to use new structure
- aider/coders/udiff_prompts.py: Will be updated to use new structure
- aider/coders/help_prompts.py: Will be updated to use new structure
- aider/coders/planner_coder.py: Will be updated to use new structure
- aider/coders/planner_prompts.py: Will be updated to use new structure

## Considerations and restrictions
- Maintain backwards compatibility where possible
- Ensure that the new structure allows for easy addition of new Coders and Edit Formats in the future
- Keep the core functionality of each Coder type (Developer, Planner, Helper) separate from the edit format logic

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

Last updated: 2024-07-20
