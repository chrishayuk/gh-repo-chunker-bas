import re

def extract_definitions(chunk_lines):
    """Extract definitions such as modules, subroutines, functions, global variables, and types from given Fortran chunk lines."""
    modules = set()
    subroutines = set()
    functions = set()
    global_vars = set()
    user_types = set()

    in_var_block = False
    in_type_block = False

    for line in chunk_lines:
        stripped_line = line.strip().upper()  # Use upper() for case-insensitivity

        # Extract modules
        if stripped_line.startswith("MODULE") and not stripped_line.startswith("MODULE PROCEDURE"):
            module_name = stripped_line.split()[1]
            modules.add(module_name)

        # Extract subroutines or functions
        if stripped_line.startswith("SUBROUTINE"):
            subroutine_name = stripped_line.split()[1].split("(")[0]
            subroutines.add(subroutine_name)
        elif stripped_line.startswith("FUNCTION"):
            function_name = stripped_line.split()[1].split("(")[0]
            functions.add(function_name)

        # Detect and handle variable/type definition sections
        if any(stripped_line.startswith(keyword) for keyword in ["REAL", "INTEGER", "CHARACTER", "LOGICAL", "COMPLEX", "DOUBLE PRECISION"]):
            in_var_block = True
            var_list = re.split(r'[:,]', stripped_line.split('::')[-1])
            global_vars.update([var.strip() for var in var_list])
        elif stripped_line.startswith("TYPE") and "=" not in stripped_line:  # Avoid confusion with TYPE casting
            in_type_block = True
            type_name = stripped_line.split()[1]
            user_types.add(type_name)
        elif stripped_line.startswith("END TYPE"):
            in_type_block = False
        elif any(stripped_line.startswith(keyword) for keyword in ["SUBROUTINE", "FUNCTION", "PROGRAM", "MODULE"]):
            in_var_block = False
        elif in_var_block and "::" in stripped_line:
            var_list = re.split(r'[:,]', stripped_line.split('::')[-1])
            global_vars.update([var.strip() for var in var_list])

    return list(modules), list(subroutines), list(functions), list(global_vars), list(user_types)
