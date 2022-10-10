program sort;
const n=24;
var a: array [0..100] of integer;
i,j,x: integer;
begin
randomize;
//ввод количества участников
writeln;
    for i:=0 to n-1 do begin
        a[i]:=i;
    end;
    for i:=0 to n-1 do begin
        write (a[i],' ');
    end;
    //sorth
    writeln;
    writeln;
    for i:=0 to n-1 do begin
        while a[i]=i do begin
            j:=random(n);
            x:=a[i];
            a[i]:=a[j];
            a[j]:=x;
        end;
    end;
    for i:=0 to n-1 do begin
        write (a[i],' ');
    end;    
writeln;
    for i:=0 to n-1 do begin
        if a[i]=i then write ('совпадает! ',i) else if i=n-1 then writeln ('всё окэ');
    end; 
end.
