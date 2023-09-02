# metadata.py
import hashlib
from .extraction import extract_definitions

def compute_file_metadata(file_path, file_content, lines, chunks, versions=[]):
    file_size = len(file_content) / (1024 * 1024)  # Size in MB.
    lines_of_code = len([line for line in lines if not line.strip().startswith("!")])
    doc_percentage = (len(lines) - lines_of_code) / len(lines) * 100 if len(lines) != 0 else 0
    hash_obj = hashlib.sha256(file_content.encode('utf-8'))
    hash_full = hash_obj.hexdigest()
    
    modules, subroutines, functions, global_vars, user_types = extract_definitions(lines)
    
    return {
        "filePath": file_path,
        "type": "f90",  # A common extension for Fortran 90/95, change if needed
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
        "modules": modules,
        "subroutines": subroutines,
        "functions": functions,
        "global_variables": global_vars,
        "user_types": user_types
    }


def calculate_chunk_metadata(chunk):
    content = chunk["content"]
    lines_of_code = len(content)
    start_line = chunk["start_line"]
    end_line = chunk["end_line"]
    parent_name = chunk.get("parent_name", None)
    parent_hash = chunk.get("parent_hash", None)

    # Extract variables (a more refined logic)
    variables = []
    for line in content:
        if "::" in line:
            var_line = line.split("::")[1].strip().split("!")[0].strip()
            for var in var_line.split(","):
                cleaned_var = var.strip()
                if "(" in cleaned_var and ")" in cleaned_var:
                    cleaned_var = cleaned_var.split("(")[0].strip() + "()"
                variables.append(cleaned_var)

    return {
        "content": content,
        "start_line": start_line,
        "end_line": end_line,
        "parent_name": parent_name,
        "parent_hash": parent_hash,
        "metadata": {
            "variables": variables,
            "linesOfCode": lines_of_code
            # ... any other metadata extraction logic ...
        }
    }
