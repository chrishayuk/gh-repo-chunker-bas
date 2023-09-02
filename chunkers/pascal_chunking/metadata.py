# metadata.py
import hashlib
from .extraction import extract_definitions

def compute_file_metadata(file_path, file_content, lines, chunks, versions=[]):
    file_size = len(file_content) / (1024 * 1024)  # Size in MB.
    lines_of_code = len([line for line in lines if not line.strip().startswith("(*") and not line.strip().startswith("{")])
    doc_percentage = (len(lines) - lines_of_code) / len(lines) * 100 if len(lines) != 0 else 0
    hash_obj = hashlib.sha256(file_content.encode('utf-8'))
    hash_full = hash_obj.hexdigest()
    
    procedures, global_vars, constants, types = extract_definitions(lines)
    
    return {
        "filePath": file_path,
        "type": "pas",
        "size": file_size,
        "linesOfCode": lines_of_code,
        "documentationPercentage": doc_percentage,
        "hashFull": hash_full,
        "hashTruncated": hash_full[:16],
        "total_lines": len(lines),
        "total_chunks": len(chunks),
        "average_chunk_size": sum([len(chunk['content']) for chunk in chunks]) / len(chunks) if chunks else 0,
        "total_variables": len(global_vars),
        "versions": versions,
        "procedures": procedures,
        "global_variables": global_vars,
        "constants": constants,
        "types": types  
    }


def calculate_chunk_metadata(chunk_data):
    chunk_content = chunk_data["content"]
    chunk_size = len(chunk_content)
    lines_of_code = chunk_size - sum(1 for line in chunk_content if line.strip().startswith("(*") or line.strip().startswith("{"))
    doc_percentage = (chunk_size - lines_of_code) / chunk_size * 100 if chunk_size != 0 else 0

    content_as_str = "\n".join(chunk_content)
    hash_obj = hashlib.sha256(content_as_str.encode('utf-8'))
    hash_full = hash_obj.hexdigest()
    hash_truncated = hash_full[:16]

    from .extraction import extract_definitions  # Import inside the function to avoid cyclic import
    procedures, global_vars, constants, types = extract_definitions(chunk_content)

    return {
        "content": chunk_content,
        "start_line": chunk_data["start_line"],
        "end_line": chunk_data["end_line"],
        "metadata": {
            "variables": global_vars,
            "procedures": procedures,
            "constants": constants,
            "types": types,
            "linesOfCode": lines_of_code,
            "documentationPercentage": doc_percentage,
            "hash": hash_full,
            "hashTruncated": hash_truncated,
            "parent_name": chunk_data.get("parent_name", None),
            "parent_hash": chunk_data.get("parent_hash", None)
        }
    }