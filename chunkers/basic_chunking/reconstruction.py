def reconstruct_program(chunked_data):
    chunks = chunked_data["chunks"]
    reconstructed_lines = []

    for chunk in chunks:
        reconstructed_lines.extend(chunk["content"])

    return "\n".join(reconstructed_lines)