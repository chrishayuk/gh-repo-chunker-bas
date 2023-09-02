import hashlib
from .extraction import extract_definitions
from .utility import (
    is_subroutine_or_function_start,
    is_large_comment_block,
    is_module_start,
    is_end_statement
)
from .metadata import calculate_chunk_metadata, compute_file_metadata

def chunk(lines, file_path, file_content, versions=[]):
    chunks = []
    current_chunk = []
    block_depth = 0
    start_line = 1
    procedure_stack = []

    for line_num, line in enumerate(lines, 1):
        stripped_line = line.strip().upper()

        if stripped_line.startswith("PROGRAM"):
            program_name = stripped_line.split()[1].strip()  # Extract program name
            procedure_stack.append(program_name)  # Add the program name to the stack

        if stripped_line.startswith("SUBROUTINE") or stripped_line.startswith("FUNCTION"):
            parent_name = procedure_stack[-1] if procedure_stack else None
            parent_hash = hashlib.sha256(parent_name.encode()).hexdigest()[:16] if parent_name else None
            
            procedure_name = stripped_line.split()[1].split('(')[0]
            procedure_stack.append(procedure_name)  # Push the procedure on top of the stack
            
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

        current_chunk.append(line)

        # Increase block depth when a new block starts and decrease when it ends
        if any(stripped_line.startswith(kw) for kw in ["DO", "IF", "SELECT CASE"]):
            block_depth += 1

        if any(stripped_line.startswith(f"END {kw}") for kw in ["DO", "IF", "SELECT CASE"]):
            block_depth -= 1

        if block_depth == 0 and any(stripped_line.startswith(f"END {kw}") for kw in ["PROGRAM", "SUBROUTINE", "FUNCTION"]):
            procedure_stack.pop()  # End of the current procedure
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
