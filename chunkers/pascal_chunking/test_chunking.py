import unittest
from .chunking import chunk, add_chunk, compute_hashes  # Replace "your_module_name" with your actual module name

class TestPascalChunkingModule(unittest.TestCase):

    def setUp(self):
        # This method will be executed before each test, you can use it to set up common resources.
        pass

    def tearDown(self):
        # This method will be executed after each test, you can use it to free up resources or perform cleanup.
        pass

    def test_chunk_simple_program(self):
        code = [
            "program HelloWorld;",
            "begin",
            "  writeln('Hello, World!');",
            "end."
        ]
        result = chunk(code)
        self.assertEqual(len(result['chunks']), 1)
        self.assertEqual(result['chunks'][0]['start_line'], 1)
        self.assertEqual(result['chunks'][0]['end_line'], 4)

    def test_chunk_procedure_inside_program(self):
        code = [
            "program SumExample;",
            "var a, b, sum: integer;",
            "procedure CalculateSum;",
            "begin",
            "  sum := a + b;",
            "end;",
            "begin",
            "  a := 5;",
            "  b := 7;",
            "  CalculateSum;",
            "  writeln(sum);",
            "end."
        ]
        result = chunk(code)
        self.assertEqual(len(result['chunks']), 3)  # One for the main program, one for the procedure, one for the main program's begin-end block

    def test_compute_hashes(self):
        chunks = [{
            "content": ["program HelloWorld;", "begin", "writeln('Hello, World!');", "end."],
            "start_line": 1,
            "end_line": 4,
            "parent_name": None,
            "parent_hash": None
        }]
        compute_hashes(chunks)
        self.assertIsNotNone(chunks[0].get("hash"))
        self.assertIsNotNone(chunks[0].get("hashTruncated"))
        self.assertEqual(len(chunks[0]["hashTruncated"]), 16)

    def test_nested_procedures(self):
        code = [
            "program NestedExample;",
            "procedure OuterProc;",
            "  procedure InnerProc;",
            "  begin",
            "    writeln('Inside InnerProc');",
            "  end;",
            "begin",
            "  InnerProc;",
            "end;",
            "begin",
            "  OuterProc;",
            "end."
        ]
        result = chunk(code)
        self.assertEqual(len(result['chunks']), 5)  # One for the main program, one for OuterProc, one for InnerProc, and one for OuterProc's begin-end block

    def test_single_line_comments(self):
        code = [
            "{ This is a single-line comment }",
            "program CommentExample;",
            "begin",
            "  writeln('Hello, World!'); { Another single-line comment }",
            "end."
        ]
        result = chunk(code)
        # Single line comments shouldn't form a separate chunk
        self.assertEqual(len(result['chunks']), 1)
        self.assertTrue("{ This is a single-line comment }" in result['chunks'][0]['content'])

    def test_multiline_comments(self):
        code = [
            "{ This is a multi-line comment",
            "  spanning multiple lines }",
            "program MultiCommentExample;",
            "begin",
            "  writeln('Hello, World!');",
            "end."
        ]
        result = chunk(code)
        # Multi-line comments shouldn't form a separate chunk
        self.assertEqual(len(result['chunks']), 1)
        self.assertTrue("{ This is a multi-line comment" in result['chunks'][0]['content'])

    def test_chunk_test_program(self):
        code = [
            "PROGRAM ChunkTest;",
            "PROCEDURE NestedProc;",
            "VAR",
            "    SomeVar: INTEGER;",
            "BEGIN",
            "    SomeVar := 0;",
            "    WHILE SomeVar < 10 DO",
            "    BEGIN",
            "        SomeVar := SomeVar + 1;",
            "    END;",
            "    IF SomeVar = 10 THEN",
            "    BEGIN",
            "        WRITE('Hello, World!');",
            "    END;",
            "END; { NestedProc }",
            "BEGIN { Main program }",
            "    NestedProc;",
            "END."
        ]
        result = chunk(code)
        # Expect chunks for main program, procedure NestedProc, and each BEGIN-END block
        self.assertEqual(len(result['chunks']), 3)

    def test_mini_chunk_test_program(self):
        code = [
            "(***", 
            "* MiniChunkTest Comment Header",
            "* This should be aligned with MiniChunkTest program",
            "*)",
            "PROGRAM MiniChunkTest;",
            "CONST",
            "  MaxValue = 10;",
            "TYPE",
            "  ValueType = 1..MaxValue;",
            "VAR",
            "  GlobalVar: ValueType;",
            "(***************************************************************************",
            "* Procedure to demonstrate chunking issue.",
            "* This should be aligned with Simple Procedure",
            "***************************************************************************)",
            "PROCEDURE SimpleProcedure;",
            "VAR",
            "  LocalVar: ValueType;",
            "BEGIN",
            "  LocalVar := 1;",
            "  WHILE LocalVar <= MaxValue DO",
            "  BEGIN",
            "    WRITE(LocalVar, ' ');",
            "    LocalVar := LocalVar + 1;",
            "  END;",
            "  IF LocalVar = MaxValue + 1 THEN",
            "  BEGIN",
            "    WRITELN('Max value reached.');",
            "  END;",
            "END; { SimpleProcedure }",
            "(***************************************************************************",
            "* Main program start.",
            "* This should be aligned with main BEGIN END block",
            "***************************************************************************)",
            "BEGIN",
            "  SimpleProcedure;",
            "END."
        ]
        result = chunk(code)
        # Expect chunks for main program, SimpleProcedure and each BEGIN-END block
        self.assertEqual(len(result['chunks']), 3)

if __name__ == "__main__":
    unittest.main()
