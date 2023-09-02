import re

def extract_definitions(chunk_lines):
    """Extract definitions such as procedures, global variables, constants, and types from given chunk lines."""
    procedures = set()
    global_vars = set()
    constants = set()
    types = set()

    in_var_block = False
    in_const_block = False
    in_type_block = False

    for line in chunk_lines:
        stripped_line = line.strip()

        # Extract procedures or functions
        if stripped_line.startswith(("PROCEDURE", "FUNCTION")):
            proc_func_split = stripped_line.split()
            if len(proc_func_split) > 1:
                proc_func_name = proc_func_split[1].split("(")[0] if "(" in proc_func_split[1] else proc_func_split[1]
                procedures.add(proc_func_name)

        # Extract global variables from VAR section
        if stripped_line.startswith("VAR"):
            in_var_block = True
        elif stripped_line.startswith("BEGIN") or any(stripped_line.startswith(keyword) for keyword in ["PROCEDURE", "FUNCTION", "TYPE", "CONST"]):
            in_var_block = False
        elif in_var_block and ":" in stripped_line:
            global_vars.update([var.strip() for var in stripped_line.split(':')[0].split(',')])

        # Extract constants from CONST section
        if stripped_line.startswith("CONST"):
            in_const_block = True
        elif any(stripped_line.startswith(keyword) for keyword in ["BEGIN", "VAR", "PROCEDURE", "FUNCTION", "TYPE"]):
            in_const_block = False
        elif in_const_block and "=" in stripped_line:
            const_name = stripped_line.split('=')[0].strip()
            constants.add(const_name)

        # Extract types from TYPE section
        if stripped_line.startswith("TYPE"):
            in_type_block = True
        elif any(stripped_line.startswith(keyword) for keyword in ["BEGIN", "VAR", "PROCEDURE", "FUNCTION", "CONST"]):
            in_type_block = False
        elif in_type_block and "=" in stripped_line:
            type_name = stripped_line.split('=')[0].strip()
            types.add(type_name)

    return list(procedures), list(global_vars), list(constants), list(types)
