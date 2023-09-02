# ==========================
# Utility Functions
# ==========================

def is_control_line(line):
    """Determines if a given line is a control line (e.g., GOTO or END)."""
    parts = line.strip().split(' ', 1)
    return parts[0] in ["GOTO", "END", "GOSUB"] or (len(parts) > 1 and parts[1].startswith(("GOTO", "END")))
