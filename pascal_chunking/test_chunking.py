import unittest
from pascal_chunking.chunking import chunk

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

        expected_output = {
            "metadata": {
                "filePath": self.file_path,
                # ... other metadata attributes
            },
            "chunks": [
                {
                    "content": [
                        "PROGRAM Test;",
                        "VAR x: integer;"
                    ],
                    # ... other chunk attributes
                },
                {
                    "content": [
                        "PROCEDURE Increment;",
                        "BEGIN",
                        "   x := x + 1;",
                        "END;"
                    ],
                    # ... other chunk attributes
                },
                {
                    "content": [
                        "BEGIN",
                        "   x := 0;",
                        "   Increment;",
                        "END."
                    ],
                    # ... other chunk attributes
                }
            ]
        }

        result = chunk(content, self.file_path, "\n".join(content))
        self.assertDictEqual(result, expected_output)

    # You can add more test cases similarly...

if __name__ == '__main__':
    unittest.main()
