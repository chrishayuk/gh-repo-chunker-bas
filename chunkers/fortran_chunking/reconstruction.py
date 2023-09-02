def reconstruct_program(chunked_data):
    chunks = chunked_data["chunks"]
    reconstructed_lines = []

    # The base indentation level
    indentation_level = 0

    # Define a helper function to handle the indentation
    def apply_indentation(line, level):
        return "    " * level + line

    in_comment_block = False
    for chunk in chunks:
        for line in chunk["content"]:
            stripped_line = line.strip().upper()  # use uppercase for all checks

            if not in_comment_block and stripped_line.startswith("!"):
                reconstructed_lines.append(apply_indentation(line.strip(), indentation_level))
                continue  # Skip further processing for comment lines

            if stripped_line in ["PROGRAM", "MODULE"]:
                reconstructed_lines.append(apply_indentation(line.strip(), indentation_level))
                indentation_level += 1
            elif stripped_line.startswith("SUBROUTINE ") or stripped_line.startswith("FUNCTION "):
                reconstructed_lines.append(apply_indentation(line.strip(), indentation_level))
                indentation_level += 1
            elif stripped_line.startswith("DO"):
                reconstructed_lines.append(apply_indentation(line.strip(), indentation_level))
                indentation_level += 1
            elif stripped_line.startswith("END DO") or stripped_line.startswith("END IF") or stripped_line.startswith("END SUBROUTINE") or stripped_line.startswith("END FUNCTION") or stripped_line.startswith("END PROGRAM") or stripped_line.startswith("END MODULE"):
                indentation_level -= 1
                reconstructed_lines.append(apply_indentation(line.strip(), indentation_level))
            elif stripped_line.startswith("IF ") or stripped_line.startswith("SELECT CASE"):
                reconstructed_lines.append(apply_indentation(line.strip(), indentation_level))
                indentation_level += 1
            elif stripped_line.startswith("CASE "):
                reconstructed_lines.append(apply_indentation(line.strip(), indentation_level))
            elif stripped_line.startswith("ELSE"):
                reconstructed_lines.append(apply_indentation(line.strip(), indentation_level))
            else:
                reconstructed_lines.append(apply_indentation(line.strip(), indentation_level))

    return "\n".join(reconstructed_lines)
