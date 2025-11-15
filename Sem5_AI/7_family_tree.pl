% -------- Facts --------
parent(john, mary).      % John is the parent of Mary
parent(john, alex).      % John is the parent of Alex
parent(mary, james).     % Mary is the parent of James
parent(mary, sophia).    % Mary is the parent of Sophia
parent(alex, emily).     % Alex is the parent of Emily
female(mary).
female(sophia).
female(emily).
male(john).
male(alex).
male(james).

% -------- Rules --------
mother(Mother, Child) :- parent(Mother, Child), female(Mother).
father(Father, Child) :- parent(Father, Child), male(Father).
sibling(X, Y) :- parent(P, X), parent(P, Y), X \= Y.
grandparent(Grandparent, Grandchild) :- parent(Grandparent, Parent), parent(Parent, Grandchild).
uncle(Uncle, NieceOrNephew) :- sibling(Uncle, Parent), male(Uncle), parent(Parent, NieceOrNephew).
aunt(Aunt, NieceOrNephew) :- sibling(Aunt, Parent), female(Aunt), parent(Parent, NieceOrNephew).
