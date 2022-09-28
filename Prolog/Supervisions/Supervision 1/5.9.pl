sum([],0).
sum([A|B],X) :- sum(B,Y), X is Y + A.

sum2([],Acc,Acc).
sum2([A|B],Acc,X) :- Y is Acc + A, sum2(B,Y,X).
sum2(X, Y) :- sum2(X, 0, Y).

biglist(1,[1]).
biglist(N,[1|T]) :- M is N-1, biglist(M, T).

?-  biglist(10000000, A), sum(A, B), print(B).
?-  biglist(10000000, A), sum2(A, B), print(B).