import importlib
import inspect


def extract_class_methods(module):
    """
    Extract all classes and their methods from a module.
    """
    methods = {}

    # Loop through all the attributes in the module
    for name, obj in inspect.getmembers(module):
        if inspect.isclass(obj):  # Check if it is a class
            class_methods = []
            for method_name, method_obj in inspect.getmembers(obj):
                if inspect.isfunction(method_obj) or inspect.ismethod(method_obj):
                    class_methods.append(method_name)
            methods[name] = class_methods
        elif inspect.isfunction(obj):  # Top-level functions
            methods[name] = 'Function'

    return methods


def load_and_extract_methods(module_name, path_to_module):
    """
    Load a module dynamically and extract methods from it.
    """
    spec = importlib.util.spec_from_file_location(module_name, path_to_module)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return extract_class_methods(module)


if __name__ == "__main__":
    # Example: Loading and inspecting CSXCAD.so
    module_name = "CSXCAD"
    path_to_module = "/home/azureuser/.local/lib/python3.10/site-packages/CSXCAD-0.6.2-py3.10-linux-x86_64.egg/CSXCAD/CSXCAD.cpython-310-x86_64-linux-gnu.so"

    methods = load_and_extract_methods(module_name, path_to_module)

    for class_name, method_list in methods.items():
        print(f"Class/Function: {class_name}")
        if isinstance(method_list, list):
            print("  Methods:")
            for method in method_list:
                print(f"    - {method}")
        else:
            print(f"  Type: {method_list}")
