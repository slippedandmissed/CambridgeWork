append([],A,A).
append([H|T],A,[H|R]) :- append(T,A,R).