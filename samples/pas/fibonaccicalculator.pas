program FibonacciCalculator;

function Fibonacci(n: LongInt): Int64;
var
    a, b, tmp: Int64;
    i: LongInt;
begin
    if n <= 1 then
        Fibonacci := n
    else
    begin
        a := 0;
        b := 1;
        for i := 2 to n do
        begin
            tmp := a + b;
            a := b;
            b := tmp;
        end;
        Fibonacci := b;
    end;
end;

var
    num: LongInt;
begin
    Write('Enter the position of Fibonacci number you want to calculate: ');
    ReadLn(num);
    
    if num < 0 then
        WriteLn('Please enter a non-negative number.')
    else
        WriteLn('Fibonacci(', num, ') = ', Fibonacci(num));
    
    ReadLn;
end.
