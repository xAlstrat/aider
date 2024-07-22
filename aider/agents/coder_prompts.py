# flake8: noqa: E501

from .base_prompts import AgentPrompts


class CoderPrompts(AgentPrompts):
    @property
    def main_system(self):
        return f"""Act as an expert software developer.
Always use best practices when coding.
Respect and use existing conventions, libraries, etc that are already present in the code base.
{{lazy_prompt}}
Take requests for changes to the supplied code.
If the request is ambiguous, ask questions.

Always reply to the user in the same language they are using.

{self.diff_format.diff_format_instructions}

Keep this info about the user's system in mind:
{{platform}}
"""

    @property
    def example_messages(self):
        return [
            dict(
                role="user",
                content="Change get_factorial() to use math.factorial",
            ),
            dict(
                role="assistant",
                content=f"""To make this change we need to modify `mathweb/flask/app.py` to:

1. Import the math package.
2. Remove the existing factorial() function.
3. Update get_factorial() to call math.factorial instead.

Here are the file updates:

{self.diff_format.format_file_diff(
    "mathweb/flask/app.py", "python", 
    chunks=[(
'''from flask import Flask''',
'''import math
from flask import Flask'''
),
(
'''def factorial(n):
    "compute factorial"

    if n == 0:
        return 1
    else:
        return n * factorial(n-1)
''', ""),
    (
"    return str(factorial(n))",
"    return str(math.factorial(n))")],
    original_full='''from flask import Flask

app = Flask(__name__)

@app.route('/<int:n>')
def factorial(n):
    "compute factorial"
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)
    return str(factorial(n))

if __name__ == '__main__':
    app.run(debug=True)
''',
    updated_full='''import math
from flask import Flask

app = Flask(__name__)

@app.route('/<int:n>')
def factorial(n):
    return str(math.factorial(n))

if __name__ == '__main__':
    app.run(debug=True)
'''
)
}
"""),
            dict(
                role="user",
                content="Refactor hello() into its own file.",
            ),
            dict(
                role="assistant",
                content=f"""To make this change we need to modify `main.py` and make a new file `hello.py`:

1. Make a new hello.py file with hello() in it.
2. Remove hello() from main.py and replace it with an import.

Here are the *SEARCH/REPLACE* blocks:

{self.diff_format.format_file_diff(
    "hello.py",
    "python",
    chunks=[("", '''def hello():
    "print a greeting"
    
    print("hello")''')],
    original_full="",
    updated_full='''def hello():
    "print a greeting"
    
    print("hello")'''
)}

{self.diff_format.format_file_diff(
    "main.py",
    "python",
    chunks=[('''def hello():
    "print a greeting"
    
    print("hello")''', "from hello import hello")],
    original_full='''def hello():
    "print a greeting"
    
    print("hello")
    
hello()''',
    updated_full='''from hello import hello
    
hello()'''
)}
""",
            ),
        ]
