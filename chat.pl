% Declare predicates as dynamic to allow runtime modifications
:- dynamic male/1.
:- dynamic female/1.
:- dynamic parent/2.
:- dynamic sibling/2.
:- dynamic pibling/2.
:- dynamic grandparent/2.

% Basic family relationship rules
% Child relationship - inverse of parent
child(Child, Parent) :- 
    parent(Parent, Child).

% Father relationship - male parent
father(Father, Child) :- 
    parent(Father, Child), 
    male(Father), 
    Father \= Child.

% Mother relationship - female parent  
mother(Mother, Child) :- 
    parent(Mother, Child), 
    female(Mother), 
    Mother \= Child.

% Enhanced sibling relationship - shares at least one parent
sibling(Person1, Person2) :-
    parent(Parent, Person1), 
    parent(Parent, Person2),  
    Person1 \= Person2.

% Brother relationship - male sibling
brother(Brother, Sibling) :- 
    sibling(Brother, Sibling), 
    male(Brother), 
    Brother \= Sibling.

% Sister relationship - female sibling
sister(Sister, Sibling) :- 
    sibling(Sister, Sibling), 
    female(Sister), 
    Sister \= Sibling.

% Son relationship - male child
son(Son, Parent) :- 
    parent(Parent, Son), 
    male(Son),
    Son \= Parent.

% Daughter relationship - female child
daughter(Daughter, Parent) :- 
    parent(Parent, Daughter), 
    female(Daughter),
    Daughter \= Parent.

% Grandparent relationship - parent of parent
grandparent(Grandparent, Grandchild) :- 
    parent(Grandparent, Parent), 
    parent(Parent, Grandchild), 
    Grandparent \= Grandchild,
    Grandparent \= Parent.

% Grandmother relationship - female grandparent
grandmother(Grandmother, Grandchild) :- 
    grandparent(Grandmother, Grandchild), 
    female(Grandmother), 
    Grandmother \= Grandchild.

% Grandfather relationship - male grandparent
grandfather(Grandfather, Grandchild) :- 
    grandparent(Grandfather, Grandchild), 
    male(Grandfather), 
    Grandfather \= Grandchild.

% Grandchild relationship - inverse of grandparent
grandchild(Grandchild, Grandparent) :- 
    grandparent(Grandparent, Grandchild),
    Grandchild \= Grandparent.

% Grandson relationship - male grandchild
grandson(Grandson, Grandparent) :- 
    grandchild(Grandson, Grandparent), 
    male(Grandson),
    Grandson \= Grandparent.

% Granddaughter relationship - female grandchild
granddaughter(Granddaughter, Grandparent) :- 
    grandchild(Granddaughter, Grandparent), 
    female(Granddaughter),
    Granddaughter \= Grandparent.

% Pibling relationship - aunt or uncle
pibling(PiblingPerson, NiblingPerson) :- 
    parent(Parent, NiblingPerson), 
    sibling(PiblingPerson, Parent),
    PiblingPerson \= NiblingPerson,
    PiblingPerson \= Parent.

% Uncle relationship - male pibling
uncle(Uncle, NieceOrNephew) :- 
    pibling(Uncle, NieceOrNephew), 
    male(Uncle),
    Uncle \= NieceOrNephew.

% Aunt relationship - female pibling
aunt(Aunt, NieceOrNephew) :- 
    pibling(Aunt, NieceOrNephew), 
    female(Aunt),
    Aunt \= NieceOrNephew.

% Nibling relationship (niece or nephew) - inverse of pibling
nibling(NiblingPerson, PiblingPerson) :- 
    pibling(PiblingPerson, NiblingPerson),
    NiblingPerson \= PiblingPerson.

% Nephew relationship - male nibling
nephew(Nephew, AuntOrUncle) :- 
    nibling(Nephew, AuntOrUncle), 
    male(Nephew),
    Nephew \= AuntOrUncle.

% Niece relationship - female nibling
niece(Niece, AuntOrUncle) :- 
    nibling(Niece, AuntOrUncle), 
    female(Niece),
    Niece \= AuntOrUncle.

% Comprehensive relatedness predicate
related(Person1, Person2) :-
    (   father(Person1, Person2)
    ;   mother(Person1, Person2)
    ;   parent(Person1, Person2)
    ;   child(Person1, Person2)
    ;   sibling(Person1, Person2)
    ;   brother(Person1, Person2)
    ;   sister(Person1, Person2)
    ;   son(Person1, Person2)
    ;   daughter(Person1, Person2)
    ;   grandparent(Person1, Person2)
    ;   grandfather(Person1, Person2)
    ;   grandmother(Person1, Person2)
    ;   grandchild(Person1, Person2)
    ;   grandson(Person1, Person2)
    ;   granddaughter(Person1, Person2)
    ;   pibling(Person1, Person2)
    ;   uncle(Person1, Person2)
    ;   aunt(Person1, Person2)
    ;   nibling(Person1, Person2)
    ;   nephew(Person1, Person2)
    ;   niece(Person1, Person2)
    ),
    Person1 \= Person2.

% Specific relationship identification predicate
relationship(Person1, Person2, father) :- father(Person1, Person2).
relationship(Person1, Person2, mother) :- mother(Person1, Person2).
relationship(Person1, Person2, parent) :- parent(Person1, Person2).
relationship(Person1, Person2, child) :- child(Person1, Person2).
relationship(Person1, Person2, sibling) :- sibling(Person1, Person2).
relationship(Person1, Person2, brother) :- brother(Person1, Person2).
relationship(Person1, Person2, sister) :- sister(Person1, Person2).
relationship(Person1, Person2, son) :- son(Person1, Person2).
relationship(Person1, Person2, daughter) :- daughter(Person1, Person2).
relationship(Person1, Person2, grandparent) :- grandparent(Person1, Person2).
relationship(Person1, Person2, grandmother) :- grandmother(Person1, Person2).
relationship(Person1, Person2, grandfather) :- grandfather(Person1, Person2).
relationship(Person1, Person2, grandchild) :- grandchild(Person1, Person2).
relationship(Person1, Person2, grandson) :- grandson(Person1, Person2).
relationship(Person1, Person2, granddaughter) :- granddaughter(Person1, Person2).
relationship(Person1, Person2, uncle) :- uncle(Person1, Person2).
relationship(Person1, Person2, aunt) :- aunt(Person1, Person2).
relationship(Person1, Person2, nephew) :- nephew(Person1, Person2).
relationship(Person1, Person2, niece) :- niece(Person1, Person2).
