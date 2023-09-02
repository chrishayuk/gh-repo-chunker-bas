# Pascal File Chunker

The Pascal File Chunker is a utility tailored for dissecting and segmenting Pascal code files into distinguishable chunks. Its core functionality extends beyond mere code fragmentation; it meticulously amasses metadata pertaining to the code, encapsulating aspects like variable employment, procedural calls, constant references, and more. Developers leveraging this utility can secure an in-depth perspective of the architecture and interdependencies within their Pascal projects.

## Features
- Methodically partitions Pascal code into coherent chunks determined by procedures, functions, and blocks.
- Derives intricate metadata regarding the code, encapsulating aspects such as:
  - Total lines of code.
  - Total chunk count.
  - Mean chunk dimensions.
  - Aggregate of unique variables.
  - Constant and type references.
- Delineates and maps procedure and function calls throughout the chunks.

## How to Use

### Prerequisites
Ensure you have Python installed.

### Steps

1. Clone or fetch this repository to your local workstation.

2. Transition to the repository's directory via your terminal.

3. Activate the script using the subsequent command:

```bash
python main.py <path_to_Pascal_file.pas>
```

Substitute <path_to_Pascal_file.pas> with the accurate path to your Pascal code file.

4. Post a successful execution, anticipate a JSON file within the same directory bearing the `.pas.json` suffix. This file encompasses the fragmented data and metadata of your Pascal code.

## Illustrative Examples

For instance, possessing a file titled `sample.pas`, chunking can be performed by executing:

```bash
python main.py sample.pas
```

Upon completion, anticipate a `sample.pas.json` file within the corresponding directory.

### Bubble Sort
To chunk bubblesort, employ:

```bash
python main.py samples/pas/bubblesort.pas
```

### Schedule
For chunking Schedule, use:

```bash
python main.py samples/pas/schedule.pas
```

## Unit Testing
Execute the following to perform unit testing for the Pascal chunker:

```bash
python -m unittest chunkers.pascal_chunking.test_chunking
```

## On the Horizon
Pending tasks include:

- Introducing repository-level runs.