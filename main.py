import sys
import json
import os
import argparse
import logging
from bas_chunker import chunk

logging.basicConfig(level=logging.INFO)

def read_file(filename):
    try:
        with open(filename, 'r') as f:
            # Return both the lines and the entire content
            return [line.strip() for line in f if line.strip() and not line.startswith("REM")], f.read()
    except Exception as e:
        logging.error(f"Failed to read file: {e}")
        sys.exit(1)

def main(args):
    lines, file_content = read_file(args.filename)
    try:
        result = chunk(lines, args.filename, file_content)
    except Exception as e:
        logging.error(f"Failed to chunk file: {e}")
        sys.exit(1)

    # Create output directory if it doesn't exist
    if not os.path.exists('output'):
        os.makedirs('output')

    # Save the result in the output folder
    output_file = os.path.join('output', os.path.basename(args.filename) + ".json")
    with open(output_file, "w") as f:
        json.dump(result, f, indent=4)

    logging.info(f"Chunked data saved to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process a BASIC code file and output a chunked JSON.')
    parser.add_argument('filename', type=str, help='The filename of the BASIC code file to be processed')
    
    args = parser.parse_args()

    if not args.filename:
        logging.error("You must specify a filename.")
        sys.exit(1)

    main(args)
