edge(node(1,1), node(6,1), 5, east).
edge(node(1,1), node(1,5), 4, south).
edge(node(6,1), node(12,1), 6, east).
edge(node(6,1), node(6,5), 4, south).
edge(node(12,1), node(12,5), 4, south).
edge(node(15,1), node(21,1), 6, east).
edge(node(15,1), node(15,5), 4, south).
edge(node(21,1), node(26,1), 5, east).
edge(node(21,1), node(21,5), 4, south).
edge(node(26,1), node(26,5), 4, south).
edge(node(1,5), node(6,5), 5, east).
edge(node(1,5), node(1,8), 3, south).
edge(node(6,5), node(9,5), 3, east).
edge(node(6,5), node(6,8), 3, south).
edge(node(1,8), node(6,8), 5, east).
edge(node(9,5), node(12,5), 3, east).
edge(node(12,5), node(15,5), 3, east).
edge(node(15,5), node(18,5), 3, east).
edge(node(18,5), node(21,5), 3, east).
edge(node(21,5), node(26,5), 5, east).
edge(node(21,5), node(21,8), 3, south).
edge(node(21,8), node(26,8), 5, east).
edge(node(26,5), node(26,8), 3, south).

edge(node(1,20),node(6,20),5,east).
edge(node(1,20),node(3,26),8,south).
edge(node(6,20),node(6,23),3,south).
edge(node(6,23),node(6,26),3,south).
edge(node(6,26),node(3,26),3,west).
edge(node(3,26),node(1,26),2,west).
edge(node(1,26),node(1,29),3,south).
edge(node(1,29),node(12,29),11,east).
edge(node(6,23),node(9,23),3,east).
edge(node(9,23),node(12,23),3,east).

edge(node(12,23),node(15,23),3,east).
edge(node(15,23),node(18,23),3,east).
edge(node(18,23),node(21,23),3,east).
edge(node(9,23),node(12,29),9,south).
edge(node(12,29),node(15,29),3,east).
edge(node(18,23),node(15,29),9,south).
edge(node(21,20),node(21,23),5,south).
edge(node(21,20),node(26,20),5,east).
edge(node(21,23),node(21,26),3,south).
edge(node(21,26),node(24,26),3,east).

edge(node(26,20),node(24,26),8,south).
edge(node(24,26),node(26,26),2,east).
edge(node(26,26),node(26,29),3,south).
edge(node(15,29),node(26,29),11,east).

edge(node(6,8),node(6,14),6,south).
edge(node(6,14),node(9,14),3,east).
edge(node(6,14),node(6,20),6,south).
edge(node(6,20),node(9,20),3,east).
edge(node(9,5),node(12,11),9,south).
edge(node(9,11),node(12,11),3,east).
edge(node(9,11),node(9,14),3,south).
edge(node(9,14),node(9,17),3,south).
edge(node(9,17),node(9,20),3,south).
edge(node(9,17),node(18,17),9,east).

edge(node(9,20),node(12,20),3,east).
edge(node(12,11),node(15,11),3,east).
edge(node(12,20),node(12,23),3,south).
edge(node(18,5),node(15,11),9,south).
edge(node(15,11),node(18,11),3,east).
edge(node(15,20),node(15,23),3,south).
edge(node(15,20),node(18,20),3,east).
edge(node(18,11),node(18,14),3,south).
edge(node(18,14),node(18,17),3,south).
edge(node(18,14),node(21,14),3,east).

edge(node(18,17),node(18,20),3,south).
edge(node(18,20),node(21,20),3,east).
edge(node(21,8),node(21,14),6,south).
edge(node(21,14),node(21,20),6,south).
edge(node(13,13),node(12,11),2,north).
edge(node(14,13),node(15,11),2,north).

opposite(south,north).
opposite(east,west).
opposite(north,south).
opposite(west,east).

findTurn(GhostNode,PacPos,InitialDir,NextDir):-
    nearestNode(PacPos,[Goal|_]),
    opposite(InitialDir,OpposeDir),
    findall(e(X,FCost),(edge(X,GhostNode,Cost,Dir),
                             Dir\=InitialDir,
                             euclidDist(X,Goal,HCost), %hCost
                       FCost is HCost+Cost),L1),
    findall(e(Y,FCost2),(edge(GhostNode,Y,Cost2,Dir),
                             Dir\=OpposeDir,
                            euclidDist(Y,Goal,HCost2),
                              FCost2 is HCost2+Cost2),L2),
    union(L1,L2,L),
    minCost(L,MinNode,_),
    move(GhostNode,MinNode,NextDir),!.

move(GhostNode,MinNode,NextDir):-
    edge(GhostNode,MinNode,_,NextDir),!.
move(GhostNode,MinNode,NextDir):-
    edge(MinNode,GhostNode,_,ODir)
    ,opposite(ODir,NextDir),
    !.

minCost([e(Node,Cost)],Node,Cost).
minCost([e(Node,Cost)|T],Node,Cost):-
    minCost(T,_,MinCost),
    Cost =< MinCost.
minCost([_|T],MinNode,MinCost):-
    minCost(T,MinNode,MinCost).


%find the distance between all nodes and ref position
findAllDistance(Nodes, Ref, Result):-
    findDist(Nodes, Ref, [], Result).
%helper fuction of find distance
findDist([],_,X,X).
findDist([H|T], Ref, Res, Result):-
    euclidDist(H,Ref,X),
    append(Res,[[H,X]],Temp),
    findDist(T,Ref,Temp, Result).

%find heuristic cost using Euclidean Distance
euclidDist(node(X1,Y1),node(X2,Y2), Distance):-
    X is X2-X1,
    Y is Y2-Y1,
    Xpow2 is X*X,
    Ypow2 is Y*Y,
    SumXY is Xpow2+Ypow2,
    Distance is sqrt(SumXY).

%find the min distance from the list of (node,distance)
minDist([X],X):-!.
minDist([[_,Dist1],[Node2,Dist2]|T], N):-
    Dist1 > Dist2,
    minDist([[Node2,Dist2]|T], N).

minDist([[Node1,Dist1], [_,Dist2]|T], N):-
    Dist1 =< Dist2,
    minDist([[Node1,Dist1]|T], N).

%find the nearest node to the Pacman position
nearestNode( PacPosition, NearestNode ):-
    findall(X,edge(X,_,_,_),Allnodes1),
    findall(Y,edge(_,Y,_,_),Allnodes2),
    append(Allnodes1, Allnodes2, AllnodesDup),
    removeDup(AllnodesDup, Allnodes),

    findAllDistance( Allnodes, PacPosition, AllDists),
    minDist(AllDists, NearestNode).

%function for removing the duplicate in
removeDup([],[]).
removeDup([H|T], [H|R]):-
    deleteForRD(H,T,S),
    removeDup(S,R).

deleteForRD(_,[],[]).
deleteForRD(X,[X|T],R):-
    deleteForRD(X,T,R).

deleteForRD(X,[H|T], [H|R]):-
    \+X=H,
    deleteForRD(X,T,R).
