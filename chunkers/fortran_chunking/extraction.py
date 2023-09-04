import re

def extract_variables_from_declaration_line(line):
    """Extract variable names from a Fortran declaration line."""
    # Extract everything after the "::" delimiter
    content_after_delimiter = line.split("::")[-1]
    # If there's an assignment in the line, only consider the left-hand side of the assignment
    if "=" in content_after_delimiter:
        content_after_delimiter = content_after_delimiter.split("=")[0]
    
    # Using regex to split the content by commas but not within brackets
    variables = re.split(r',(?![^()]*\))', content_after_delimiter)
    
    # Clean and format variables
    cleaned_vars = []
    for var in variables:
        var = var.strip()
        # Check and reformat variable representations with dimensions
        if "(" in var and ")" in var:
            var = var.split("(")[0] + "()"
        # Ensure that variable names start with a valid character (avoiding numbers or special characters)
        if re.match(r"^[A-Za-z_]", var):
            cleaned_vars.append(var)
    return cleaned_vars

def extract_definitions(chunk_lines):
    """Extract definitions such as modules, subroutines, functions, global variables, and types from given Fortran chunk lines."""
    modules = set()
    subroutines = set()
    functions = set()
    global_vars = set()
    user_types = set()

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

        # Handle user types
        if stripped_line.startswith("TYPE") and "=" not in stripped_line:  # Avoid confusion with TYPE casting
            type_name = stripped_line.split()[1]
            user_types.add(type_name)

        # Extract global variables
        declaration_keywords = ["REAL", "INTEGER", "CHARACTER", "LOGICAL", "COMPLEX", "DOUBLE PRECISION"]
        if any(stripped_line.startswith(keyword) for keyword in declaration_keywords) and "INTENT" not in stripped_line and "PARAMETER" not in stripped_line:
            global_vars.update(extract_variables_from_declaration_line(stripped_line))

    return list(modules), list(subroutines), list(functions), list(global_vars), list(user_types)
