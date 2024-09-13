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
    classes = {}

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            class_name = node.name
            methods = []
            for sub_node in ast.iter_child_nodes(node):
                if isinstance(sub_node, ast.FunctionDef):
                    method_name = sub_node.name
                    docstring = ast.get_docstring(sub_node)
                    methods.append((method_name, docstring))
            classes[class_name] = methods
        elif isinstance(node, ast.FunctionDef):
            func_name = node.name
            docstring = ast.get_docstring(node)
            if not func_name.startswith("__"):  # Ignore dunder (__) methods
                functions.append((func_name, docstring))

    return comments, functions, classes


def generate_markdown(comments, functions, classes, file_name):
    """
    Generate markdown format output for the extracted data.
    """
    md_content = f"# Documentation for {file_name}\n\n"

    # Add class details
    if classes:
        md_content += "## Classes and Methods\n"
        for class_name, methods in classes.items():
            md_content += f"### Class: {class_name}\n"
            for method_name, docstring in methods:
                if docstring:
                    md_content += f"#### Method: {method_name}\n"
                    md_content += f"```\n{docstring}\n```\n"
                else:
                    md_content += f"#### Method: {method_name}\n"
                    md_content += "_No documentation available_\n"
            md_content += "\n"

    # Add standalone functions
    if functions:
        md_content += "## Functions\n"
        for func_name, docstring in functions:
            if docstring:
                md_content += f"### Function: {func_name}\n"
                md_content += f"```\n{docstring}\n```\n"
            else:
                md_content += f"### Function: {func_name}\n"
                md_content += "_No documentation available_\n"
        md_content += "\n"

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
                    comments, functions, classes = extract_comments_and_definitions(file_path)
                    markdown_content = generate_markdown(comments, functions, classes, file)
                    md_file.write(markdown_content)
                    md_file.write("\n\n")


if __name__ == "__main__":
    openems_path = "/home/azureuser/.cache/JetBrains/PyCharm2023.3/python_stubs/-32419096/openEMS/"
    csxcad_path = "/home/azureuser/.cache/JetBrains/PyCharm2023.3/python_stubs/-32419096/CSXCAD/"

    # Output markdown files
    openems_output = "../doc_dumps/openEMS_pycharm_stubs_docs_2.md"
    csxcad_output = "../doc_dumps/CSXCAD_pycharm_stubs_docs_2.md"

    main(openems_path, openems_output)
    main(csxcad_path, csxcad_output)
