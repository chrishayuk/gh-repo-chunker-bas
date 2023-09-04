import hashlib
from .metadata import calculate_chunk_metadata, compute_file_metadata

import re

def chunk(lines, file_path, file_content, versions=[]):
    chunks = []
    current_chunk = []
    block_depth = 0
    start_line = 1
    procedure_stack = []

    def get_parent_hash(parent_name):
        return hashlib.sha256(parent_name.encode()).hexdigest()[:16] if parent_name else None

    def is_block_start(line):
        return re.match(r"^\s*(PROGRAM|SUBROUTINE|FUNCTION|MODULE|CONTAINS)", line, re.I)

    def get_name_from_block(line):
        matches = re.search(r"\b(PROGRAM|SUBROUTINE|FUNCTION|MODULE)\s+(\w+)", line, re.I)
        return matches.groups()[1] if matches else None

    def add_chunk(start, end, content):
        parent_name = procedure_stack[-1] if procedure_stack else None
        parent_hash = get_parent_hash(parent_name)
        if content:  # Add the chunk only if it has content
            chunks.append(calculate_chunk_metadata({
                "content": content,
                "start_line": start,
                "end_line": end,
                "parent_name": parent_name,
                "parent_hash": parent_hash
            }))

    is_inside_c_comment = False
    for line_num, line in enumerate(lines, 1):
        stripped_line = line.strip().upper()

        # Handle C-style comments
        if stripped_line.startswith("/*"):
            is_inside_c_comment = True
        if is_inside_c_comment:
            if "*/" in stripped_line:
                is_inside_c_comment = False
            continue

        # Handle regular Fortran comments
        if stripped_line.startswith(('!', 'C', '//')):
            continue

        # Adjust block depth
        if any(stripped_line.startswith(kw) for kw in ["DO", "IF", "SELECT CASE"]):
            block_depth += 1
        if any(stripped_line.startswith(f"END {kw}") for kw in ["DO", "IF", "SELECT CASE"]):
            block_depth -= 1

        # Block start: PROGRAM, SUBROUTINE, FUNCTION, MODULE, CONTAINS
        if is_block_start(stripped_line):
            if 'CONTAINS' not in stripped_line:
                if procedure_stack:
                    add_chunk(start_line, line_num - 1, current_chunk)
                    current_chunk = []
                start_line = line_num
                procedure_name = get_name_from_block(stripped_line)
                if procedure_name:
                    procedure_stack.append(procedure_name)

        current_chunk.append(line)

        # End of block: PROGRAM, SUBROUTINE, FUNCTION, MODULE
        if block_depth == 0 and any(stripped_line.startswith(f"END {kw}") for kw in ["PROGRAM", "SUBROUTINE", "FUNCTION", "MODULE"]):
            if 'MODULE' in stripped_line:
                continue
            add_chunk(start_line, line_num, current_chunk)
            current_chunk = []
            start_line = line_num + 1
            if procedure_stack:
                procedure_stack.pop()

    # Handle any leftover content
    if current_chunk:
        add_chunk(start_line, line_num, current_chunk)

    file_metadata = compute_file_metadata(file_path, file_content, lines, chunks, versions)

    return {
        "metadata": file_metadata,
        "chunks": chunks
    }
