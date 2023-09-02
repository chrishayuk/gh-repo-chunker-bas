program AdvancedProgram;

uses
  SysUtils;

type
  MathOperations = object
    function Add(a, b: Integer): Integer;
    function Subtract(a, b: Integer): Integer;
  end;

  StringOperations = object
    function Concatenate(const str1, str2: string): string;
    function StringLength(const str: string): Integer;
  end;

function MathOperations.Add(a, b: Integer): Integer;
begin
  Result := a + b;
end;

function MathOperations.Subtract(a, b: Integer): Integer;
begin
  Result := a - b;
end;

function StringOperations.Concatenate(const str1, str2: string): string;
begin
  Result := str1 + str2;
end;

function StringOperations.StringLength(const str: string): Integer;
begin
  Result := Length(Trim(str));
end;

var
  x, y, result: Integer;
  str1, str2, combined: string;
  mathOps: MathOperations;
  stringOps: StringOperations;

begin
  // Math operations
  x := 5;
  y := 3;
  result := mathOps.Add(x, y);
  WriteLn('The sum of ', x, ' and ', y, ' is ', result);
  result := mathOps.Subtract(x, y);
  WriteLn('The difference between ', x, ' and ', y, ' is ', result);

  // String operations
  str1 := 'Hello, ';
  str2 := 'world!';
  combined := stringOps.Concatenate(str1, str2);
  WriteLn(combined);
end.
