program main;
        
var result,result2,result3:integer;
        
function sum(a,b:integer):integer;
	begin
		sum := a + b;
	end;

function minus(a,b:integer):integer;
	begin
		minus := a - b;
	end;

function test(a,b:integer):integer;
	var x,y:integer;
	begin
		x := sum(a,b);
		y := minus(a,b);
		test := x*y
	end;
        
begin
	result := sum(1,2); 
	result2 := minus(5,4);
	result3 := test(result, result2)
end.