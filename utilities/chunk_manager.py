import importlib
import logging

class ChunkManager:

    @staticmethod
    def process_chunking(file_config, lines, filename, file_content):
        # Dynamically import the module based on configuration
        module_name = file_config['chunker']
        try:
            chunker_module = importlib.import_module(module_name)
        except ImportError as e:
            logging.error(f"Failed to import module '{module_name}': {e}")
            return None
        
        chunking_function = getattr(chunker_module, file_config["chunker_function"], None)
        if not chunking_function:
            logging.error(f"Chunking function '{file_config['chunker_function']}' not found!")
            return None
        
        try:
            return chunking_function(lines, filename, file_content, versions=file_config["versions"])
        except Exception as e:
            logging.error(f"Failed to chunk file: {e}")
            return None
