s(z).
s(s(A)) :- s(A).

prim(0,z).
prim(A,s(B)) :- prim(X,B), A is X+1. % I don't know how to avoid that "is"

plus(A,z,A).
plus(z,A,A).
plus(A,s(B),s(C)) :- plus(A,B,C).
plus(s(A),B,s(C)) :- plus(A,B,C).

mult(_,z,z).
mult(z,_,z).
mult(A,s(B),C) :- mult(A,B,X), plus(X,A,C).
mult(s(A),B,C) :- mult(A,B,X), plus(X,B,C).