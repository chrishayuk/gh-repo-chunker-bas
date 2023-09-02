import hashlib
from .extraction import extract_variables
from .utility import is_control_line

def add_chunk(chunks, current_chunk, current_start, current_end):
    """Adds a chunk to the chunks list if current_chunk is not empty."""
    if current_chunk:
        chunks.append({
            "content": current_chunk,
            "start_line": current_start,
            "end_line": current_end
        })


def combine_small_chunks(chunks):
    """Combines chunks of size 1 with their subsequent chunk."""
    i = 0
    while i < len(chunks) - 1:
        if len(chunks[i]["content"]) == 1:
            chunks[i + 1]["content"] = chunks[i]["content"] + chunks[i + 1]["content"]
            chunks[i + 1]["start_line"] = chunks[i]["start_line"]
            del chunks[i]
        else:
            i += 1


def compute_hashes(chunks):
    """Computes hashes for each chunk."""
    for chunk in chunks:
        chunk_content = '\n'.join(chunk["content"])
        hash_obj = hashlib.sha256(chunk_content.encode('utf-8'))
        hash_full = hash_obj.hexdigest()
        chunk["hash"] = hash_full
        chunk["hashTruncated"] = hash_full[:16]


def update_references(chunks):
    """Updates the chunks with reference information (which chunk references which)."""
    for idx, chunk in enumerate(chunks):
        chunk["line_count"] = len(chunk["content"])
        for line in chunk["content"]:
            if "GOTO" in line:
                referenced_line = line.split("GOTO")[1].strip().split()[0]
                for target_idx, target_chunk in enumerate(chunks):
                    if not referenced_line:
                        print(f"Error: referenced_line is None for line: {line}")
                    if not target_chunk["start_line"] or not target_chunk["end_line"]:
                        print(f"Error: start or end line is None for target_chunk: {target_chunk}")

                    if target_chunk["start_line"] <= referenced_line <= target_chunk["end_line"]:
                        chunk.setdefault("references", {}).setdefault("goto", {})[referenced_line] = {
                            "chunk_index": f"Chunk {target_idx + 1}",
                            "hashTruncated": target_chunk["hashTruncated"]
                        }


def calculate_metadata(chunks, all_vars, file_path, file_content, versions):
    """Computes metadata about the chunks and variables."""
    total_lines = sum(len(chunk["content"]) for chunk in chunks)
    lines_of_code = total_lines - sum(1 for line in file_content.split('\n') if is_control_line(line))
    doc_percentage = (total_lines - lines_of_code) / total_lines * 100 if total_lines != 0 else 0
    file_size = len(file_content.encode('utf-8')) / (1024 * 1024)
    hash_obj = hashlib.sha256(file_content.encode('utf-8'))
    hash_full = hash_obj.hexdigest()
    hash_truncated = hash_full[:16]
    
    return {
        "filePath": file_path,
        "type": "bas",
        "size": file_size,
        "linesOfCode": lines_of_code,
        "documentationPercentage": doc_percentage,
        "hashFull": hash_full,
        "hashTruncated": hash_truncated,
        "total_lines": total_lines,
        "total_chunks": len(chunks),
        "average_chunk_size": total_lines / len(chunks) if chunks else 0,
        "total_variables": len(all_vars),
        "versions": versions
    }


def chunk(lines, file_path, file_content, versions=[]):
    """Main chunking function that divides lines into chunks and computes metadata."""
    chunks = []
    current_chunk = []
    current_start = None
    all_vars = set()

    for line_num, line in enumerate(lines, start=1):  # Using enumerate to get the line number
        all_vars.update(extract_variables(line))
        current_end = line.split()[0]
        
        if current_start is None:  # Initialize current_start with the line number of the first line
            current_start = str(line_num)  # Convert line number to string to match the format of current_end

        if is_control_line(line):
            current_chunk.append(line)
            add_chunk(chunks, current_chunk, current_start, current_end)
            current_chunk = []
            current_start = None  # Reset current_start so that it can be set on the next loop iteration
        else:
            current_chunk.append(line)

    add_chunk(chunks, current_chunk, current_start, current_end)
    combine_small_chunks(chunks)
    compute_hashes(chunks)
    update_references(chunks)
    metadata = calculate_metadata(chunks, all_vars, file_path, file_content, versions)
    
    return {
        "metadata": metadata,
        "chunks": chunks
    }

