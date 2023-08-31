import logging
import json

class FileHandler:
    
    @staticmethod
    def read_file(filename):
        try:
            with open(filename, 'r') as f:
                lines = [line.strip() for line in f if line.strip() and not line.startswith("REM")]
                f.seek(0)  # Reset the file pointer to the start of the file
                content = f.read()
                return lines, content
        except Exception as e:
            logging.error(f"Failed to read file: {e}")
            return None, None
    
    @staticmethod
    def write_json_to_output(data, filename):
        import os
        import json

        if not os.path.exists('output'):
            os.makedirs('output')

        output_file = os.path.join('output', os.path.basename(filename) + ".json")
        with open(output_file, "w") as f:
            json.dump(data, f, indent=4)
        
        return output_file

    @staticmethod
    def write_text_to_output(data, filename, file_type):
        import os

        if not os.path.exists('output'):
            os.makedirs('output')

        base_name, _ = os.path.splitext(os.path.basename(filename))
        
        # Split the base_name again in case the original file was like 'sample.bas.json'
        base_name, _ = os.path.splitext(base_name)
        
        output_file_path = os.path.join('output', base_name + "." + file_type) 

        with open(output_file_path, 'w') as f:
            f.write(data)
        
        return output_file_path