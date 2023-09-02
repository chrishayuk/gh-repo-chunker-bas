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

def chunk(lines, file_path, file_content, versions=[]):
    chunks = []
    current_chunk = []
    block_depth = 0
    in_comment_block = False
    procedure_comment_block = []
    start_line = 1
    procedure_stack = []

    def is_next_line_procedure_or_function(lines, current_index):
        for i in range(current_index, len(lines)):
            stripped = lines[i].strip()
            if not (stripped.startswith("(*") or stripped.startswith("{")):
                return is_procedure_or_function_start(stripped)
        return False

    for line_num, line in enumerate(lines, 1):
        stripped_line = line.strip()

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
            parent_name = procedure_stack[-1] if procedure_stack else None
            parent_hash = hashlib.sha256(parent_name.encode()).hexdigest()[:16] if parent_name else None

            procedure_name = stripped_line.split()[1].split('(')[0]

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
        block_depth += stripped_line.count("BEGIN") - stripped_line.count("END")

        if block_depth == 0 and is_end(stripped_line):
            if procedure_stack:
                # Check if current line is indeed the end of the top-most procedure on the stack
                top_procedure = procedure_stack[-1]
                if stripped_line.endswith(f"{top_procedure} END;"):
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
