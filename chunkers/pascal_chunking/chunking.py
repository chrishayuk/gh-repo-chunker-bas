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
import hashlib

def chunk(lines, file_path=None, file_content=None, versions=[]):
    chunks = []
    current_chunk = []
    block_depth = 0
    start_line = 1
    procedure_stack = []
    comment_cache = []

    def is_procedure_or_function_start(line):
        return re.match(r"^\s*(procedure|function)\s+\w+", line, re.I) is not None

    def get_parent_hash(parent_name):
        return hashlib.sha256(parent_name.encode()).hexdigest()[:16] if parent_name else None

    in_comment = False

    for line_num, line in enumerate(lines, 1):  # Enumerate from 1 for correct line numbers.
        stripped_line = line.strip().lower()

        if stripped_line.startswith("(*"):
            in_comment = True

        if in_comment:
            comment_cache.append(line)
            if stripped_line.endswith("*)"):
                in_comment = False
            continue  # Continue regardless of whether the comment ended to prevent double-counting
        
        # If the line is not part of a comment and not blank, it might be the start of a new chunk.
        if not stripped_line:
            continue

        # For a program's main declaration or procedure, we add any preceding comments to the chunk.
        if re.match(r"^\s*program\s+\w+", stripped_line, re.I) or is_procedure_or_function_start(stripped_line) or (stripped_line == "begin" and not procedure_stack and not current_chunk):
            # If we start a new procedure or program and there is already content in the current chunk, create a new chunk.
            if current_chunk:
                chunks.append({
                    "content": current_chunk.copy(),
                    "start_line": start_line,
                    "end_line": line_num - len(comment_cache) - 1,
                    "parent_name": None,
                    "parent_hash": None
                })
                current_chunk = []
                start_line = line_num - len(comment_cache)
            current_chunk.extend(comment_cache)
            comment_cache.clear()

        procedure_name = None
        if is_procedure_or_function_start(stripped_line):
            procedure_name = re.search(r"\b(procedure|function)\s+(\w+)", stripped_line, re.I).groups()[1]
            procedure_stack.append(procedure_name)

        current_chunk.append(line)

        # Adjust block depth
        block_depth += stripped_line.count("begin")
        block_depth -= stripped_line.count("end")

        # If we encounter an 'end' and our block depth is zero, we've finished a procedure or the main program
        if block_depth == 0 and "end" in stripped_line:
            chunks.append({
                "content": current_chunk.copy(),
                "start_line": start_line,
                "end_line": line_num,
                "parent_name": procedure_stack[-1] if procedure_stack else None,
                "parent_hash": get_parent_hash(procedure_stack[-1] if procedure_stack else None)
            })
            current_chunk = []
            start_line = line_num + 1
            if procedure_stack:
                procedure_stack.pop()

    # If there's any leftover content, add it to the chunks
    if current_chunk:
        chunks.append({
            "content": current_chunk,
            "start_line": start_line,
            "end_line": line_num,
            "parent_name": procedure_stack[-1] if procedure_stack else None,
            "parent_hash": get_parent_hash(procedure_stack[-1] if procedure_stack else None)
        })

    return {
        "metadata": {},
        "chunks": chunks
    }