# BASIC File Chunker

The BASIC File Chunker is a utility designed to analyze and segment BASIC code files into chunks. It not only breaks down the code but also provides metadata about the code such as variable usage, control flow references, and more. This utility helps developers gain insights into the structure and dependencies within their BASIC codebase.

## Features
- Splits BASIC code into logical chunks based on control statements.
- Computes metadata about the entire code, including:
  - Total lines of code.
  - Number of chunks.
  - Average chunk size.
  - Total unique variables.
- Identifies and maps the GOTO references across chunks.

## How to Use

### Prerequisites
Make sure you have Python installed.

### Steps

1. Clone or download this repository to your local machine.

2. Navigate to the repository directory in your terminal.

3. Run the script using the following command:

```bash
python main.py <path_to_BASIC_file.bas>
```

Replace `<path_to_BASIC_file.bas>` with the path to your BASIC file.

4. Upon successful execution, you'll find a JSON file in the same directory with the `.bas.json` extension. This file contains the chunked data and metadata of your BASIC code.

## Example

Suppose you have a file named `sample.bas`. You can chunk it by running:

```bash
python main.py sample.bas
```

After running, you'll find a `sample.bas.json` file in the same directory.
