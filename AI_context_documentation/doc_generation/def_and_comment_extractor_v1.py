import os
import ast
import inspect
import re


def extract_comments_and_definitions(file_path):
    """
    Extract comments and function definitions from a Python file.
    """
    with open(file_path, 'r') as file:
        content = file.read()

    # Extract comments using regex
    comments = re.findall(r'#.*', content)

    # Parse the file to get function signatures and docstrings
    tree = ast.parse(content)
    functions = []

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            func_name = node.name
            docstring = ast.get_docstring(node)
            if docstring:
                functions.append((func_name, docstring))

    return comments, functions


def generate_markdown(comments, functions, file_name):
    """
    Generate markdown format output for the extracted data.
    """
    md_content = f"# Documentation for {file_name}\n\n"

    # Add comments
    if comments:
        md_content += "## Comments\n"
        for comment in comments:
            md_content += f"- {comment}\n"
        md_content += "\n"

    # Add function signatures and docstrings
    if functions:
        md_content += "## Functions and Docstrings\n"
        for func_name, docstring in functions:
            md_content += f"### {func_name}\n"
            md_content += f"```\n{docstring}\n```\n"

    return md_content


def main(root_directory, output_file):
    """
    Walk through the root directory and parse all Python files.
    """
    with open(output_file, 'w') as md_file:
        for subdir, _, files in os.walk(root_directory):
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(subdir, file)
                    comments, functions = extract_comments_and_definitions(file_path)
                    markdown_content = generate_markdown(comments, functions, file)
                    md_file.write(markdown_content)
                    md_file.write("\n\n")


if __name__ == "__main__":
    openems_path = "/home/azureuser/.cache/JetBrains/PyCharm2023.3/python_stubs/-32419096/openEMS/"
    csxcad_path = "/home/azureuser/.cache/JetBrains/PyCharm2023.3/python_stubs/-32419096/CSXCAD/"

    # Output markdown files
    openems_output = "../doc_dumps/openEMS_pycharm_stubs_docs.md"
    csxcad_output = "../doc_dumps/CSXCAD_pycharm_stubs_docs.md"

    main(openems_path, openems_output)
    main(csxcad_path, csxcad_output)

