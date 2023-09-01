import hashlib
from .extraction import extract_definitions, extract_variables
from .utility import is_procedure_or_function_start, is_begin, is_end

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

def calculate_metadata(chunks, all_vars, file_path, file_content, versions):
    total_lines = sum(len(chunk["content"]) for chunk in chunks)
    lines_of_code = total_lines - sum(1 for line in file_content.split('\n') if is_begin(line) or is_end(line))
    doc_percentage = (total_lines - lines_of_code) / total_lines * 100 if total_lines != 0 else 0
    file_size = len(file_content.encode('utf-8')) / (1024 * 1024)
    hash_obj = hashlib.sha256(file_content.encode('utf-8'))
    hash_full = hash_obj.hexdigest()
    hash_truncated = hash_full[:16]

    procedures, global_vars, constants, types = extract_definitions(file_content.split('\n'))

    # Format the results for procedures, constants, and types
    procedures = [p[0] for p in procedures]
    constants = [c[0] for c in constants]
    types = [t[0] for t in types]

    return {
        "filePath": file_path,
        "type": "pas",
        "size": file_size,
        "linesOfCode": lines_of_code,
        "documentationPercentage": doc_percentage,
        "hashFull": hash_full,
        "hashTruncated": hash_truncated,
        "total_lines": total_lines,
        "total_chunks": len(chunks),
        "average_chunk_size": total_lines / len(chunks) if chunks else 0,
        "total_variables": len(all_vars),
        "versions": versions,
        "procedures": procedures,
        "global_variables": global_vars,
        "constants": constants,
        "types": types
    }

def chunk(lines, file_path, file_content, versions=[]):
    chunks = []
    current_chunk = []
    block_depth = 0
    current_start = 1
    in_procedure_or_function = False
    in_global_declaration = True
    in_comment = False
    procedures, global_vars, constants, types = extract_definitions(lines)

    for line_num, line in enumerate(lines, start=1):
        stripped_line = line.strip()

        # Handle multiline comments
        if stripped_line.startswith("(*") or stripped_line.startswith("{"):
            in_comment = True
        if in_comment and (stripped_line.endswith("*)") or stripped_line.endswith("}")):
            in_comment = False
        if in_comment:
            current_chunk.append(line)
            continue

        # If we detect a new procedure or function
        if is_procedure_or_function_start(stripped_line):
            if in_global_declaration:
                add_chunk(chunks, current_chunk, current_start, line_num-1, global_vars, procedures, constants, types)
                current_chunk = []
            in_procedure_or_function = True
            in_global_declaration = False
            current_start = line_num

        current_chunk.append(line)

        # Handle block depth for procedures, functions and main body
        if stripped_line.startswith("BEGIN"):
            block_depth += 1
        elif stripped_line.startswith("END;"):
            block_depth -= 1

            if in_procedure_or_function and block_depth == 0:
                add_chunk(chunks, current_chunk, current_start, line_num, global_vars, procedures, constants, types)
                current_chunk = []
                current_start = line_num + 1
                in_procedure_or_function = False

    # Handle the main program block or any residual content
    if current_chunk:
        add_chunk(chunks, current_chunk, current_start, line_num, global_vars, procedures, constants, types)

    all_vars = extract_variables(lines)
    compute_hashes(chunks)
    metadata = calculate_metadata(chunks, all_vars, file_path, file_content, versions)

    return {
        "metadata": metadata,
        "chunks": chunks
    }
