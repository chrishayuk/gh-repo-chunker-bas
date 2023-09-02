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

import hashlib

def chunk(lines, file_path, file_content, versions=[]):
    chunks = []
    current_chunk = []
    block_depth = 0
    in_comment_block = False
    procedure_comment_block = []
    start_line = 1
    procedure_stack = []
    in_function_or_procedure = False

    def is_large_comment_block(line):
        return line.startswith("(*") or line.startswith("{")

    def is_next_line_procedure_or_function(lines, current_index):
        for i in range(current_index, len(lines)):
            stripped = lines[i].strip()
            if not (stripped.startswith("(*") or stripped.startswith("{")):
                return is_procedure_or_function_start(stripped)
        return False

    def is_end(line):
        return line.strip().lower().startswith("end;") and block_depth == 0

    def is_procedure_or_function_end(line):
        return line.strip().lower().startswith("end;") and in_function_or_procedure and block_depth == 0 and not in_comment_block

    def is_procedure_or_function_start(line):
        return "function" in line.lower() or "procedure" in line.lower()

    def get_parent_hash(parent_name, current_chunk):
        return hashlib.sha256(parent_name.encode()).hexdigest()[:16] if parent_name else None

    for line_num, line in enumerate(lines, 1):
        stripped_line = line.strip()

        if "PROGRAM" in stripped_line:
            parent_name = stripped_line.split()[1].strip(" ;")
            procedure_stack.append(parent_name)

        if "object" in stripped_line:
            parent_name = stripped_line.split("=")[0].strip()
            procedure_stack.append(parent_name)

        if is_large_comment_block(stripped_line):
            in_comment_block = True

        if in_comment_block:
            procedure_comment_block.append(line)
            if stripped_line.endswith("*)") or stripped_line.endswith("}"):
                in_comment_block = False
                if not is_next_line_procedure_or_function(lines, line_num):
                    current_chunk.extend(procedure_comment_block)
                    procedure_comment_block = []
            continue

        if is_procedure_or_function_start(stripped_line) and block_depth == 0:
            in_function_or_procedure = True
            if "." in stripped_line:
                object_name = stripped_line.split(".")[0].strip()
                if object_name in procedure_stack:
                    procedure_stack.pop()
                procedure_stack.append(object_name)

            parent_name = procedure_stack[-1] if procedure_stack else None
            procedure_name = stripped_line.split()[1].split('(')[0]
            procedure_stack.append(procedure_name)

            if current_chunk:
                chunks.append(calculate_chunk_metadata({
                    "content": current_chunk,
                    "start_line": start_line,
                    "end_line": line_num - 1,
                    "parent_name": parent_name if "object" not in current_chunk[0] else None,
                    "parent_hash": get_parent_hash(parent_name, current_chunk)
                }))
                current_chunk = []
                start_line = line_num

            if procedure_comment_block:
                current_chunk.extend(procedure_comment_block)
                procedure_comment_block = []

        current_chunk.append(line)

        block_depth += stripped_line.lower().count("begin") - stripped_line.lower().count("end")

        if block_depth == 0 and is_procedure_or_function_end(stripped_line):
            parent_name = procedure_stack[-2] if len(procedure_stack) > 1 else None
            procedure_stack.pop()
            in_function_or_procedure = False

        elif block_depth == 0 and is_end(stripped_line):
            parent_name = procedure_stack[-1] if len(procedure_stack) > 1 else None
            if "end" in stripped_line.lower() and procedure_stack[-1] != parent_name:
                procedure_stack.pop()
            chunks.append(calculate_chunk_metadata({
                "content": current_chunk,
                "start_line": start_line,
                "end_line": line_num,
                "parent_name": parent_name if "object" not in current_chunk[0] else None,
                "parent_hash": get_parent_hash(parent_name, current_chunk)
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

