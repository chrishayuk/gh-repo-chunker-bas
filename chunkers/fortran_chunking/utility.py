# ==========================
# Utility Functions for Fortran
# ==========================

def is_comment(line):
    """Checks if the line is a comment in Fortran."""
    stripped_line = line.strip().upper()  # Use upper() for case-insensitivity
    return stripped_line.startswith('!')

def is_begin(line):
    """Checks if the line indicates the start of a block in Fortran."""
    stripped_line = line.strip().upper()
    return stripped_line.startswith(('SUBROUTINE', 'FUNCTION', 'MODULE', 'DO', 'IF', 'SELECT CASE', 'PROGRAM'))

def is_end_statement(line):
    """Checks if the line indicates the end of a block in Fortran."""
    stripped_line = line.strip().upper()
    return 'END' in stripped_line  # can be END, END DO, END IF, END FUNCTION, etc.

def is_subroutine_or_function_start(line):
    """Check if a given line starts with a subroutine or function definition in Fortran."""
    stripped_line = line.strip().upper()
    return stripped_line.startswith(('SUBROUTINE', 'FUNCTION'))

def is_module_start(line):
    """Check if a given line starts with a module definition in Fortran."""
    stripped_line = line.strip().upper()
    return stripped_line.startswith('MODULE')

def is_large_comment_block(line):
    """Check if a given line starts a multi-line comment block in Fortran."""
    # Fortran does not typically have multi-line comments like Pascal. 
    # However, you can handle long inline comments here if needed.
    # For simplicity, this will just handle inline comments using "!"
    return line.strip().upper().startswith('!')

def is_loop_or_conditional(line):
    """Check if the line starts a loop or conditional block in Fortran."""
    stripped_line = line.strip().upper()
    return stripped_line.startswith(('DO', 'IF', 'SELECT CASE'))

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
