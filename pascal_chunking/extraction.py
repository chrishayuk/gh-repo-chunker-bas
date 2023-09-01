import re

def extract_definitions(lines):
    procedures = []
    global_vars = []
    constants = []
    types = []

    in_var_block = False
    for i, line in enumerate(lines):
        line_stripped = line.strip().lower()

        # Procedure extraction
        procedure_match = re.match(r'^procedure (\w+)', line_stripped)
        if procedure_match:
            procedures.append((procedure_match.group(1), i+1))

        # Variable block determination
        if line_stripped.startswith("var"):
            in_var_block = True
        elif not line_stripped or line_stripped.startswith("begin") or line_stripped.startswith("procedure"):
            in_var_block = False

        # Variable extraction
        if in_var_block:
            variable_match = re.match(r'^([\w\s,]+):', line_stripped)
            if variable_match:
                vars_list = variable_match.group(1).split(",")
                for var in vars_list:
                    global_vars.append(var.strip())

        # Constant extraction
        const_match = re.match(r'^(\w+)\s*=', line_stripped)
        if const_match:
            constants.append((const_match.group(1), i+1))

        # Type extraction
        type_match = re.match(r'^(\w+)\s*=', line_stripped)
        if type_match and "array" in line_stripped:
            types.append((type_match.group(1), i+1))

    return procedures, global_vars, constants, types

def extract_variables(lines):
    variables = set()
    inside_var_block = False
    for line in lines:
        if "var" in line.lower():
            inside_var_block = True
        if inside_var_block and (";" in line):
            parts = line.split(':')
            if len(parts) > 1:
                var_names = parts[0].split(',')
                for name in var_names:
                    variables.add(name.strip())
            if ";" in line:
                inside_var_block = False
    return variables
