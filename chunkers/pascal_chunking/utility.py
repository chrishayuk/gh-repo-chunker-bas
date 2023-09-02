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
    """Check if a given line starts with a procedure or function definition in Pascal."""
    return line.strip().startswith("PROCEDURE") or line.strip().startswith("FUNCTION")

def is_large_comment_block(line):
    """Check if a given line starts a multi-line comment block in Pascal."""
    return line.startswith("(*") or line.startswith("{")

def is_loop_or_conditional(line):
    """Check if the line starts a loop or conditional block."""
    line = line.strip().lower()
    return line.startswith(("for", "while", "if"))

def safe_get_line(lines, index):
    """Safely retrieves a line from a list of lines by index."""
    try:
        return lines[index]
    except IndexError:
        return ""

def safe_get_next_line(lines, current_index):
    """Safely retrieves the next line from a list of lines."""
    if current_index < len(lines) - 1:
        return lines[current_index + 1]
    else:
        return ""
