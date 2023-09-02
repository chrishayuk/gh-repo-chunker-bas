import unittest

# Import from the bas_chunker.py module
from chunkers.basic_chunking.chunking import chunk
from chunkers.basic_chunking.reconstruction import reconstruct_program
from chunkers.basic_chunking.utility import is_control_line
from chunkers.basic_chunking.extraction import extract_variables

class TestBasicChunking(unittest.TestCase):

    def test_extract_variables(self):
        self.assertEqual(extract_variables("A = 5"), {"A", "=", "5"})
        self.assertEqual(extract_variables("GOTO 10"), {"GOTO", "10"})

    def test_is_control_line(self):
        self.assertTrue(is_control_line("GOTO 10"))
        self.assertTrue(is_control_line("END"))
        self.assertFalse(is_control_line("A = 5"))
        self.assertFalse(is_control_line("PRINT A"))

    def test_chunking_and_reconstruction(self):
        lines = [
            "10 A = 5",
            "20 B = 6",
            "30 PRINT A + B",
            "40 GOTO 60",
            "50 END",
            "60 PRINT 'Finished'"
        ]
        file_content = "\n".join(lines)
        chunked_data = chunk(lines, "test.bas", file_content)
        reconstructed = reconstruct_program(chunked_data)
        for content in chunked_data["chunks"]:
            print(content["content"])
        self.assertEqual(reconstructed, file_content)

    def test_metadata(self):
        lines = [
            "10 A = 5",
            "20 B = 6",
            "30 PRINT A + B",
            "40 GOTO 60",
            "50 END",
            "60 PRINT 'Finished'"
        ]
        file_content = "\n".join(lines)
        chunked_data = chunk(lines, "test.bas", file_content)
        metadata = chunked_data['metadata']
        self.assertEqual(metadata['filePath'], "test.bas")
        self.assertEqual(metadata['type'], "bas")
        self.assertEqual(metadata['linesOfCode'], 4)  # Exclude control lines
        self.assertEqual(metadata['total_lines'], 6)  # Total lines in the file
        self.assertEqual(metadata['total_chunks'], 2)  # Based on the logic, this should be 3 chunks

    # Additional tests can be added here, such as verifying hashing, references, and other specifics

if __name__ == '__main__':
    unittest.main()
