![](https://github.com/georgekouzi/DirectedWeightedGraph_onPython/blob/main/image/%E2%80%8F%E2%80%8F1.PNG?raw=true)
# Directed Weighted Graph in Python 
.

### my code in Peyton language VS my code in Java language VS networkx library .
----
This project comes to compare code that written in Java to code that written in Peyton (current code)


-------------------------------------------------------------------------------------

This project is done to compare the run times of a directed weighted graph in java language, Peyton language and the networkx library that exists in Python and allows us to create graphs and perform various operations on this graph, the shown code in this project is in Peyton language, the code in java language at the following link : https://github.com/georgekouzi/pokemon_Game.git -(in src folder choose dataStructure and algorithms folder, the Comparison file you can find in the test folder).
Comparison files can be found in the Comparison_files folder. 

in this project We present a class of directed weighted graph in the Peyton language and another class that executes algorithms on graphs.
in addition you can findnode class that produces the nodes in the graph.

-------------------------------------------------------------------------------------


#### first we explain how actually we create graph and how different information about the graph can be obtained using the algorithms shortestPath,connected_components,connected_component. 

## The functions in the DiGraph class and the description about them :

1) __v_size(self) -> int -__ This function returns the amount of the nodes that exist in the graph.
--------------------------------------------------------------------------
2) __e_size(self) -> int -__ This function returns the amount of the edges that exist in the graph.
------------------------------------------------------------
3) __get_all_v(self) -> dict: -__ This function return a dictionary of all the nodes in the graph.
---------------------------------------------------------
4) __all_in_edges_of_node(self, id1: int) -> dict -__ This function return a dictionary of all the nodes connected to (into) node_id. the function gets a source node key and returns all the parents node that connect to this id1 node. If there are no parents nodes that connect to this node or this node does not exist at all the function will return an empty dictionary, the dictionary output need see like that:    
{0: 1.1, 2: 1.3, 3: 10} - dictionary of key(the parents node) and value( weighted of the edge- 
__destination node(id1)__ __<------- __all the source node__.

---------------------------------------------------------------
5) __all_out_edges_of_node(self, id1: int) -> dict -__ This function return a dictionary of all the nodes connected to (from) node_id. the function gets a source node key and returns all the neighbors  node that connect to this id1 node. If there are no neighbors  nodes that connect to this node or this node does not exist at all the function will return an empty dictionary, the dictionary output need see like that:    
{0: 1.1, 2: 1.3, 3: 10} - dictionary of key(the neighbors  node) and value( weighted of the edge- 
__source  node(id1)__ __------>__ __destination node__ .
------------------------------------------------------------------------------------
6) __get_mc(self) -> int -__ This function returns to the amount of operations that we did in the graph.
----------------------------------------------------------------------------------------
7) __add_edge(self, id1: int, id2: int, weight: float) -> bool -__ This function receives a Key of source node (id1), key of destination(id2) node and weight(weight) of the new edge. and creat a new edge and adds it to the graph dictionary and update the mode Count(mc) and finally return true . if the edge already exists the function will do nothing and return false. this function also checks if the weight is positive (i.e. does not allow insertion of negative weight.
--------------------------------------------------
8) __add_node(self, node_id: int, pos: tuple = None) -> bool -__ This function receives a new node and adds it to the _graph dictionary and update the mode Count(mc) and finally return true. If the node already exists in the graph dictionary nothing will be done and the function return false.
--------------------------------------------------------
9) __remove_node(self, node_id: int) -> bool -__ This function receives a key of a particular node and deletes it from the graph. This function searches for all the edges that have this destination node node_id and all the edges that have this sorce node (node_id) . Finally it will delete the node from the _graph dictionary and retune true .
If this node does not exist the function will return false.
----------------------------------------------------------------
10) __remove_edge(self, node_id1: int, node_id2: int) -> bool -__ -This function gets two keys, a source node_id1 and a destination node_id2, the function checks if this edge exists and deletes this edge and returns true. If the edge does not exist the function returns false.

## More explanation for how the game work : 
https://github.com/georgekouzi/pokemon_Game/wiki/pokemon-game

## for more informetion about the projact : 
https://github.com/georgekouzi/pokemon_Game/wiki.

----

#### The project was written by Dolev Saadia and George Kouzi:



https://github.com/georgekouzi


https://github.com/dolevsaadia

----



