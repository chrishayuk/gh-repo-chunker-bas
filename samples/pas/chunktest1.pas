PROGRAM ChunkTest;

PROCEDURE NestedProc;
VAR
    SomeVar: INTEGER;
BEGIN
    SomeVar := 0;
    WHILE SomeVar < 10 DO
    BEGIN
        SomeVar := SomeVar + 1;
    END;
    IF SomeVar = 10 THEN
    BEGIN
        WRITE('Hello, World!');
    END;
END; { NestedProc }

BEGIN { Main program }
    NestedProc;
END.
