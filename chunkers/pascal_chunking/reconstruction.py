def reconstruct_program(chunked_data):
    chunks = chunked_data["chunks"]
    reconstructed_lines = []

    # The base indentation level
    indentation_level = 0

    # Define a helper function to handle the indentation
    def apply_indentation(line, level):
        return "    " * level + line

    construct_stack = []
    in_comment_block = False
    for chunk in chunks:
        for line in chunk["content"]:
            stripped_line = line.strip().upper()  # use uppercase for all checks

            if not in_comment_block and (stripped_line.startswith("(*") or stripped_line.startswith("{")):
                in_comment_block = True

            # If in a comment block, append line without changing indentation level
            if in_comment_block:
                reconstructed_lines.append(apply_indentation(stripped_line, indentation_level))
                if stripped_line.endswith("*)") or stripped_line.endswith("}"):
                    in_comment_block = False
                continue  # Skip further processing for comment lines

            if stripped_line in ["CONST", "TYPE", "VAR", "PROGRAM"]:
                reconstructed_lines.append(apply_indentation(line.strip(), indentation_level))
                indentation_level += 1
            elif stripped_line.startswith("PROCEDURE ") or stripped_line.startswith("FUNCTION "):
                reconstructed_lines.append(apply_indentation(line.strip(), indentation_level))
                indentation_level += 1
            elif stripped_line.startswith("BEGIN"):
                reconstructed_lines.append(apply_indentation(line.strip(), indentation_level))
                indentation_level += 1
            elif stripped_line.startswith("END"):
                indentation_level -= 1
                reconstructed_lines.append(apply_indentation(line.strip(), indentation_level))
            elif stripped_line.startswith("IF ") or stripped_line.startswith("FOR ") or stripped_line.startswith("WHILE "):
                reconstructed_lines.append(apply_indentation(line.strip(), indentation_level))
                if not line.strip().endswith('then') and not line.strip().endswith('do'):
                    indentation_level += 1
            elif stripped_line.startswith("ELSE"):
                reconstructed_lines.append(apply_indentation(line.strip(), indentation_level))
            else:
                reconstructed_lines.append(apply_indentation(line.strip(), indentation_level))

    return "\n".join(reconstructed_lines)
