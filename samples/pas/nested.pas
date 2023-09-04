program NestedDemo;

var
  globalVar: Integer;

(* This is a multi-line comment 
   that has some strange
   format.
{ This is an embedded comment inside another one. Weird, right?
  It also spans multiple lines, just to increase the confusion. }
   This is still part of the multi-line comment. *)
procedure OuterProcedure;
var
  outerVar: Integer;
  
  procedure InnerProcedure;
  var
    innerVar: Integer;
    
    function InnermostFunction(x: Integer): Integer;
    var
      retVal: Integer;  (* A local variable to hold the return value *)
    begin
      (* Comment inside a function *)
      retVal := x + outerVar + globalVar;
      InnermostFunction := retVal; (* Set the function's return value here *)
    end;
  
  begin { InnerProcedure }
    innerVar := 10;
    outerVar := InnermostFunction(innerVar);
    WriteLn('Value from innermost function: ', outerVar);
  end;

begin { OuterProcedure }
  outerVar := 5;
  InnerProcedure;
end;

begin { Main program }
  globalVar := 3;
  OuterProcedure;
end.