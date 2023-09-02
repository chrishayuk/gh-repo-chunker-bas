import sys
import argparse
import logging
import os
import json

from utilities.file_handler import FileHandler
from utilities.config_manager import ConfigManager
from utilities.chunk_manager import ChunkManager
from chunkers.pascal_chunking.chunking import chunk as pascal_chunk
from chunkers.pascal_chunking.reconstruction import reconstruct_program as reconstruct_pascal
from chunkers.basic_chunking.chunking import chunk as basic_chunk
from chunkers.basic_chunking.reconstruction import reconstruct_program as reconstruct_basic

logging.basicConfig(level=logging.INFO)

def main(args):
    # Check if reconstruction is needed
    if args.reconstruct:
        with open(args.filename, 'r') as f:
            chunked_data = json.load(f)
        
        # Extract the type of the file from the metadata
        file_type = chunked_data.get("metadata", {}).get("type")
        
        if file_type == "bas":
            reconstructed_code = reconstruct_basic(chunked_data)
        elif file_type == "pas":
            reconstructed_code = reconstruct_pascal(chunked_data)
        else:
            logging.error(f"Reconstruction not supported for type '{file_type}'.")
            sys.exit(1)
        
        # Use FileHandler to save the reconstructed code
        output_file = FileHandler.write_text_to_output(reconstructed_code, args.filename, file_type)
        logging.info(f"Reconstructed code saved to {output_file}")
        return

    # Use FileHandler to read file
    lines, file_content = FileHandler.read_file(args.filename)
    
    if not lines or not file_content:
        sys.exit(1)

    file_extension = os.path.splitext(args.filename)[1]

    # Use ConfigManager to get file config
    file_config = ConfigManager.get_config_for_file(file_extension)
    if not file_config:
        logging.error(f"No configuration found for files with extension '{file_extension}'.")
        sys.exit(1)

    # Use ChunkManager to get processed chunks
    result = ChunkManager.process_chunking(file_config, lines, args.filename, file_content)
    if not result:
        sys.exit(1)
        
    # Use FileHandler to save output
    output_file = FileHandler.write_json_to_output(result, args.filename)
    logging.info(f"Chunked data saved to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process a code file and output a chunked JSON or reconstruct from chunked JSON.')
    parser.add_argument('filename', type=str, help='The filename of the code file to be processed or reconstructed from')
    parser.add_argument('--reconstruct', action='store_true', help='Reconstruct a program from chunked JSON file')
    
    args = parser.parse_args()

    if not args.filename:
        logging.error("You must specify a filename.")
        sys.exit(1)

    main(args)
