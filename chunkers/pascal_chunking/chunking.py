import hashlib
from .extraction import extract_definitions


from .utility import (is_procedure_or_function_start, 
                      safe_get_line, 
                      safe_get_next_line, 
                      is_large_comment_block, 
                      is_begin, 
                      is_end)
from .metadata import calculate_chunk_metadata, compute_file_metadata

def add_chunk(chunks, current_chunk, current_start, current_end, global_vars, procedures, constants, types):
    """Adds a chunk to the chunks list if current_chunk is not empty with its metadata."""
    
    if current_chunk:
        chunk_content = '\n'.join(current_chunk)
        chunk_metadata = {"variables": [], "procedures": [], "constants": [], "types": []}

        for var in global_vars:
            if var in chunk_content:
                chunk_metadata["variables"].append(var)
        for proc in procedures:
            if proc[0] in chunk_content:
                chunk_metadata["procedures"].append(proc[0])
        for const in constants:
            if const[0] in chunk_content:
                chunk_metadata["constants"].append(const[0])
        for typ in types:
            if typ[0] in chunk_content:
                chunk_metadata["types"].append(typ[0])

        chunks.append({
            "content": current_chunk.copy(),
            "start_line": current_start,
            "end_line": current_end,
            "metadata": chunk_metadata
        })

def compute_hashes(chunks):
    for chunk in chunks:
        chunk_content = '\n'.join(chunk["content"])
        hash_obj = hashlib.sha256(chunk_content.encode('utf-8'))
        hash_full = hash_obj.hexdigest()
        chunk["hash"] = hash_full
        chunk["hashTruncated"] = hash_full[:16]

import re

import re
import hashlib

def chunk(lines, file_path=None, file_content=None, versions=[]):
    chunks = []
    current_chunk = []
    block_depth = 0
    start_line = 1
    program_stack = []
    comment_cache = []
    program_name = None

    def is_program_start(line):
        return re.match(r"^\s*program\s+\w+", line, re.I) is not None

    def get_parent_hash(parent_name):
        return hashlib.sha256(parent_name.encode()).hexdigest()[:16] if parent_name else None

    for line_num, line in enumerate(lines, 1):  # Enumerate from 1 for correct line numbers.
        stripped_line = line.strip().lower()

        # Handling comments
        if stripped_line.startswith("!"):
            comment_cache.append(line)
            continue

        # Skip blank lines
        if not stripped_line:
            continue

        # For a program's main declaration, save its name and add any preceding comments to the chunk.
        if is_program_start(stripped_line):
            program_name = re.search(r"\bprogram\s+(\w+)", stripped_line, re.I).groups()[0]
            if current_chunk:
                chunk_data = {
                    "content": current_chunk.copy(),
                    "start_line": start_line,
                    "end_line": line_num - len(comment_cache) - 1,
                    "parent_name": program_stack[-1] if program_stack else None,
                    "parent_hash": get_parent_hash(program_stack[-1] if program_stack else None)
                }
                chunks.append(calculate_chunk_metadata(chunk_data))
                current_chunk = []
                start_line = line_num - len(comment_cache)
            current_chunk.extend(comment_cache)
            comment_cache.clear()

        current_chunk.append(line)

        # Adjust block depth
        block_depth += stripped_line.count("subroutine")
        block_depth -= stripped_line.count("end subroutine")

        # If we encounter an 'end' with block depth of zero, finish the procedure or the main program
        if block_depth == 0 and ("end program" in stripped_line or "end subroutine" in stripped_line):
            chunk_data = {
                "content": current_chunk.copy(),
                "start_line": start_line,
                "end_line": line_num,
                "parent_name": program_stack[-1] if program_stack else None,
                "parent_hash": get_parent_hash(program_stack[-1] if program_stack else None)
            }
            chunks.append(calculate_chunk_metadata(chunk_data))
            current_chunk = []
            start_line = line_num + 1
            if program_stack:
                program_stack.pop()

    # Handle any leftover content
    if current_chunk:
        chunk_data = {
            "content": current_chunk,
            "start_line": start_line,
            "end_line": line_num,
            "parent_name": program_stack[-1] if program_stack else None,
            "parent_hash": get_parent_hash(program_stack[-1] if program_stack else None)
        }
        chunks.append(calculate_chunk_metadata(chunk_data))

    file_metadata = compute_file_metadata(file_path, "".join(lines), lines, chunks, versions)

    return {
        "metadata": file_metadata,
        "chunks": chunks
    }

