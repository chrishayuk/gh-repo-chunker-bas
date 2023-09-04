(*** 
* MiniChunkTest Comment Header
* This should be aligned with MiniChunkTest program
**)
PROGRAM MiniChunkTest;

CONST
  MaxValue = 10;

TYPE
  ValueType = 1..MaxValue;

VAR
  GlobalVar: ValueType;

(***************************************************************************
* Procedure to demonstrate chunking issue.
* This should be aligned with Simple Procedure
***************************************************************************)
PROCEDURE SimpleProcedure;
VAR
  LocalVar: ValueType;
BEGIN
  LocalVar := 1;
  WHILE LocalVar <= MaxValue DO
  BEGIN
    WRITE(LocalVar, ' ');
    LocalVar := LocalVar + 1;
  END;

  IF LocalVar = MaxValue + 1 THEN
  BEGIN
    WRITELN('Max value reached.');
  END;
END; { SimpleProcedure }

(***************************************************************************
* Main program start.
* This should be aligned with main BEGIN END block
***************************************************************************)
BEGIN
  SimpleProcedure;
END.
