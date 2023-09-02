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

def chunk(lines, file_path, file_content, versions=[]):
    chunks = []
    current_chunk = []
    block_depth = 0
    start_line = 1
    procedure_stack = []

    def is_procedure_or_function_start(line):
        return re.match(r"^\s*(procedure|function)\s+\w+", line, re.I) is not None

    def get_parent_hash(parent_name):
        return hashlib.sha256(parent_name.encode()).hexdigest()[:16] if parent_name else None

    for line_num, line in enumerate(lines, 1):
        stripped_line = line.strip().lower()

        # Handling Program declarations
        if re.match(r"^\s*program", stripped_line):
            parent_name = stripped_line.split()[1].strip(" ;")
            procedure_stack.append(parent_name)

        # Handling procedure or function start
        if is_procedure_or_function_start(stripped_line):
            if current_chunk:  # Store the current chunk
                chunks.append({
                    "content": current_chunk.copy(),
                    "start_line": start_line,
                    "end_line": line_num - 1,
                    "parent_name": procedure_stack[-1] if procedure_stack else None,
                    "parent_hash": get_parent_hash(procedure_stack[-1] if procedure_stack else None)
                })
                current_chunk.clear()
            start_line = line_num
            parent_name = re.search(r"\b(procedure|function)\s+(\w+)", stripped_line, re.I).groups()[1]
            procedure_stack.append(parent_name)

        # Adjust block depth
        block_depth += stripped_line.count("begin")
        block_depth -= stripped_line.count("end")

        current_chunk.append(line)

        # Handle end of chunks based on depth
        if block_depth == 0 and "end" in stripped_line:
            chunks.append({
                "content": current_chunk.copy(),
                "start_line": start_line,
                "end_line": line_num,
                "parent_name": procedure_stack[-2] if len(procedure_stack) > 1 else procedure_stack[-1],
                "parent_hash": get_parent_hash(procedure_stack[-2] if len(procedure_stack) > 1 else procedure_stack[-1])
            })
            current_chunk.clear()
            start_line = line_num + 1
            if len(procedure_stack) > 1:  # Pop the last procedure or function only if there's a parent
                procedure_stack.pop()

    # Placeholder for compute_file_metadata
    def compute_file_metadata(file_path, file_content, lines, chunks, versions):
        return {}

    file_metadata = compute_file_metadata(file_path, file_content, lines, chunks, versions)
    return {
        "metadata": file_metadata,
        "chunks": chunks
    }
