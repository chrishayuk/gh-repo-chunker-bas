import unittest
from chunkers.pascal_chunking.chunking import chunk

class TestPascalChunking(unittest.TestCase):

    def setUp(self):
        self.file_path = "test.pas"

    def test_simple_procedure(self):
        content = [
            "PROGRAM Test;",
            "VAR x: integer;",
            "PROCEDURE Increment;",
            "BEGIN",
            "   x := x + 1;",
            "END;",
            "BEGIN",
            "   x := 0;",
            "   Increment;",
            "END."
        ]

        result = chunk(content, self.file_path, "\n".join(content))

        # Verifying chunk content as it's deterministic and crucial
        self.assertEqual(len(result["chunks"]), 3)
        self.assertEqual(result["chunks"][0]["content"], ['PROGRAM Test;', 'VAR x: integer;'])
        self.assertEqual(result["chunks"][1]["content"], ['PROCEDURE Increment;', 'BEGIN', '   x := x + 1;', 'END;'])
        self.assertEqual(result["chunks"][2]["content"], ['BEGIN', '   x := 0;', '   Increment;', 'END.'])

        # Verifying metadata: we won't check every attribute, but a few critical ones to ensure function is working as expected
        self.assertEqual(result["metadata"]["filePath"], self.file_path)
        self.assertEqual(result["metadata"]["type"], "pas")
        self.assertEqual(result["metadata"]["total_chunks"], 3)
        self.assertEqual(result["metadata"]["total_lines"], 10)
        self.assertEqual(result["metadata"]["linesOfCode"], 10)  # Exclude BEGIN and END lines


    def test_no_procedure_or_function(self):
        content = ["PROGRAM Test;", "VAR x: integer;", "BEGIN", "   x := 0;", "END."]
        result = chunk(content, self.file_path, "\n".join(content))
        # TODO: Assertions based on the expected output...

    def test_nested_procedure(self):
        content = [
            "PROGRAM Test;", 
            "PROCEDURE Outer;", 
            "   PROCEDURE Inner;", 
            "   BEGIN", 
            "      // Inner logic", 
            "   END;", 
            "BEGIN", 
            "   // Outer logic", 
            "END;", 
            "BEGIN", 
            "   Outer;", 
            "END."
        ]
        result = chunk(content, self.file_path, "\n".join(content))
        # TODO: Assertions based on the expected output...

    def test_multiline_comments(self):
        content = ["PROGRAM Test;", "(* This is a", "multiline comment *)", "BEGIN", "   // Do something", "END."]
        result = chunk(content, self.file_path, "\n".join(content))
        # TODO: Assertions based on the expected output...

    def test_multiple_procedures(self):
        content = [
            "PROGRAM Test;", 
            "PROCEDURE First;", 
            "BEGIN", 
            "   // First logic", 
            "END;", 
            "PROCEDURE Second;", 
            "BEGIN", 
            "   // Second logic", 
            "END;", 
            "BEGIN", 
            "   First;", 
            "   Second;", 
            "END."
        ]
        result = chunk(content, self.file_path, "\n".join(content))
        # TODO: Assertions based on the expected output...

    def test_no_main_block(self):
        content = [
            "PROCEDURE Solo;", 
            "BEGIN", 
            "   // Solo logic", 
            "END;"
        ]
        result = chunk(content, self.file_path, "\n".join(content))
        # TODO: Assertions based on the expected output...

    def test_empty_input(self):
        content = []
        result = chunk(content, self.file_path, "\n".join(content))
        # TODO: Assertions based on the expected output...

    def test_incomplete_code(self):
        content = ["PROGRAM Test;", "VAR x: integer;", "BEGIN", "   x := 0;"]
        result = chunk(content, self.file_path, "\n".join(content))
        # TODO: Assertions based on the expected output...

if __name__ == '__main__':
    unittest.main()
