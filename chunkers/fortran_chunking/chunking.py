import hashlib

from .extraction import extract_definitions
from .utility import (
    is_subroutine_or_function_start,
    safe_get_line,
    safe_get_next_line,
    is_large_comment_block,
    is_module_start,
    is_end_statement
)
from .metadata import calculate_chunk_metadata, compute_file_metadata

def chunk(lines, file_path, file_content, versions=[]):
    chunks = []
    current_chunk = []
    block_depth = 0
    in_comment_block = False
    procedure_comment_block = []
    start_line = 1
    procedure_stack = []

    def is_next_line_subroutine_or_function(lines, current_index):
        for i in range(current_index, len(lines)):
            stripped = lines[i].strip().upper()
            if not stripped.startswith("!"):
                return is_subroutine_or_function_start(stripped)
        return False

    for line_num, line in enumerate(lines, 1):
        stripped_line = line.strip().upper()  # Make Fortran parsing case-insensitive

        if is_large_comment_block(stripped_line):
            in_comment_block = True

        if in_comment_block:
            procedure_comment_block.append(line)
            if stripped_line.endswith("!"):
                in_comment_block = False
                if not is_next_line_subroutine_or_function(lines, line_num):
                    current_chunk.extend(procedure_comment_block)
                    procedure_comment_block = []
            continue

        if (is_subroutine_or_function_start(stripped_line) or is_module_start(stripped_line)) and block_depth == 0:
            parent_name = procedure_stack[-1] if procedure_stack else None
            parent_hash = hashlib.sha256(parent_name.encode()).hexdigest()[:16] if parent_name else None

            procedure_name = stripped_line.split()[1]  # Assuming name is the second word in the line

            if current_chunk:
                chunks.append(calculate_chunk_metadata({
                    "content": current_chunk,
                    "start_line": start_line,
                    "end_line": line_num - 1,
                    "parent_name": parent_name,
                    "parent_hash": parent_hash
                }))
                current_chunk = []
                start_line = line_num

            procedure_stack.append(procedure_name)

            if procedure_comment_block:
                current_chunk.extend(procedure_comment_block)
                procedure_comment_block = []

        current_chunk.append(line)

        # This is a simple block depth counter; real-world Fortran can be more complex
        if any(keyword in stripped_line for keyword in ["SUBROUTINE", "FUNCTION", "MODULE", "DO", "IF", "SELECT CASE"]):
            block_depth += 1
        if is_end_statement(stripped_line):
            block_depth -= 1

        if block_depth == 0 and is_end_statement(stripped_line):
            if procedure_stack:
                # Check if current line is indeed the end of the top-most procedure on the stack
                top_procedure = procedure_stack[-1]
                if stripped_line.endswith(f"END {top_procedure}"):
                    procedure_stack.pop()

            parent_name = procedure_stack[-1] if procedure_stack else None
            parent_hash = hashlib.sha256(parent_name.encode()).hexdigest()[:16] if parent_name else None

            chunks.append(calculate_chunk_metadata({
                "content": current_chunk,
                "start_line": start_line,
                "end_line": line_num,
                "parent_name": parent_name,
                "parent_hash": parent_hash
            }))

            start_line = line_num + 1
            current_chunk = []

    if current_chunk:
        parent_name = procedure_stack[-1] if procedure_stack else None
        parent_hash = hashlib.sha256(parent_name.encode()).hexdigest()[:16] if parent_name else None

        chunks.append(calculate_chunk_metadata({
            "content": current_chunk,
            "start_line": start_line,
            "end_line": line_num,
            "parent_name": parent_name,
            "parent_hash": parent_hash
        }))

    file_metadata = compute_file_metadata(file_path, file_content, lines, chunks, versions)

    return {
        "metadata": file_metadata,
        "chunks": chunks
    }
