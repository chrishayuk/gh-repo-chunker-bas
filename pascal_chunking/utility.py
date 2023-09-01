# ==========================
# Utility Functions
# ==========================
def is_comment(line):
    """Checks if the line is a comment."""
    stripped_line = line.strip()
    return stripped_line.startswith('{') or stripped_line.startswith('//')

def is_begin(line):
    """Checks if the line indicates the start of a block."""
    return line.strip().lower().startswith('begin')

def is_end(line):
    """Checks if the line indicates the end of a block."""
    stripped_line = line.strip().lower()
    return stripped_line.endswith('end;') or stripped_line.endswith('end.')

def is_procedure_or_function_start(line):
    """Checks if the line indicates the start of a procedure or function."""
    return line.strip().lower().startswith(('procedure', 'function'))

def is_loop_or_conditional(line):
    """Check if the line starts a loop or conditional block."""
    line = line.strip().lower()
    return line.startswith(("for", "while", "if"))
