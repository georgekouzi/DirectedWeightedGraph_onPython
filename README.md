![](https://github.com/georgekouzi/DirectedWeightedGraph_onPython/blob/main/image/%E2%80%8F%E2%80%8F1.PNG?raw=true)
# Directed Weighted Graph in Python 
.

### my code in Peyton language VS my code in Java language VS networkx library .
For results and for to see the tables comparisons, click on this link:
https://github.com/georgekouzi/DirectedWeightedGraph_onPython/wiki/comparisons

To see my computer specifications click on the following link:
https://github.com/georgekouzi/DirectedWeightedGraph_onPython/wiki/my-computer-specifications

----
This project comes to compare code that written in Java to code that written in Peyton (current code)


-------------------------------------------------------------------------------------

This project is done to compare the run times of a directed weighted graph in java language, Peyton language and the networkx library that exists in Python and allows us to create graphs and perform various operations on this graph, the shown code in this project is in Peyton language, the code in java language at the following link : https://github.com/georgekouzi/pokemon_Game.git -(in src folder choose dataStructure and algorithms folder, the Comparison file you can find in the test folder).
Comparison files can be found in the Comparison_files folder. 

in this project We present a class of directed weighted graph in the Peyton language and another class that executes algorithms on graphs.
in addition you can findnode class that produces the nodes in the graph.

-------------------------------------------------------------------------------------
## In order for this project to work, a 3 library must be installed:
1) numpy library in version 1.19.3
2) matplotlib library in version 3.3.3
3) Networkx library in version 2.5

## class DiGraph:
This class creates an directed weighted graph. In order to create this graph we used two Node classes that we wrote.

### The functions in the DiGraph class and the description about them :

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

## class GraphAlgo:
This class allows you to do operations on a graph that require different algorithms.

### The functions in the GraphAlgo class and the description about them :

1) __get_graph(self) -> GraphInterface -__  This function return your graph.
---------------------

2) __load_from_json(self, file_name: str) -> bool -__ Load this json file (directed weighted graph). This function path of json file name on the computer. The default path to this file is in the project folder. we use json lib- Which allows us to extract the information from the json file that we need and read it and create a new graph . and its data can be used to recreate the object in memory. The information we want to load is: a dictionary of list of all edges and list of all nodes. the run time is: O(E*V)- E - edges and V-nodes. we use json folder to get json file load.
if the save succdicessfully the function return true else return false.

--------------------------------------------------------
3) __save_to_json(self, file_name: str) -> bool -__  Saves this directed weighted graph to this json file name(file_name:str). This function path of json file name on the computer. The default path to this file is in the project folder(src). we use json lib- Which allows us to extract the information we need and write it into the json file. The information we want to keep is: dictionary of list of all the edges and list of all the nodes. 
the run time is: O(E*V)- E - edges and V-nodes. if the save succdicessfully the function return true else return false.
--------------------------------------------------------
4) __shortest_path(self, id1: int, id2: int) -> (float, list) -___ returns tuple of the length of the shortest path between src to dest and the shortest pat list between src to dest - as an ordered List of nodes: source--> n1-->n2-->...destination. 
In order to find the shortest path from source node to destination node we will use the algorithm of dijkstra.. if src==dest we return (inf, [id1])
or if no path between the node -->  we return (inf, None).

----------------------------------------
5) ___dijkstra(self, id_src) ->dict -__ This algorithm makes it possible to go over a weighted directed graph And find the cheapest ways from the source node to the rest of the graph nodes. The weights in the graph symbolize distance. The shortest route between two points means the route with the lowest amount of weights between the two vertices. we use inner class that call nodeAlgo to save all the data that dijkstra algorithm need. Ran time- O(E*log(V)) because we create PriorityQueue and compare the node by the minimum distareturns - 
the function return a dictionary of all the node with information about the chipsets paths from the source node  to all the node in the graph.
-----------------------------------------------
6) __connected_component(self, id1: int) -> list -__ This function checks if there is a Circular  Path from node id1 node to all the nodes With Dfs Algorithm- this is an improved DFS called Tarjan Algorithm. after use DFS Algorithm we get list of list of all the phath in this component. Tarjan_Algo dictionary - serves data Structure: stack ,lowlink ,count and st_trace. 
run time O(E + V): E- the number of ribs, V- the number of nodes.
------------------------------------------------------------
7) __connected_components(self) -> List[list]-__ This function checks if there is a Path from each node to all the nodes With Dfs Algorithm- this is an improved DFS called Tarjan Algorithm. after use DFS Algorithm we get list of list of all the phath in this component  if the size of the list  equal to 1 So the graph is strongly connected and can be reached from any node to any other node. Tarjan_Algo dictionary - serves data Structure: stack ,lowlink ,count and st_trace. 
run time O(E + V): E- the number of ribs, V- the number of nodes.
-------------------------------------------------
8) __dfs(self, n, tarjan_dict) -> dict -__ this algorithm makes it possible to go over a weighted directed graph the node stack, which starts out empty and stores the history of nodes explored but not yet committed to a strongly connected component. as nodes are not popped as the search returns up the tree; they are only popped when an entire strongly connected component has been found. The outermost loop searches each node that has not yet been visited, ensuring that nodes which are not reachable from the first node are still eventually traversed. finding all successors from the node v, and reporting all strongly connected components of that subgraph. When each node finishes recursing, if its lowlink is still set to its index, then it is the root node of a strongly connected component, formed by all of the nodes above it on the stack. The algorithm pops the stack up to and including the current node, and presents all of these nodes as a strongly connected component. Note that v.lowlink := min(v.lowlink, w.index) is the correct way to update v.lowlink if w is on stack. Because w is on the stack already, (v, w) is a back-edge in the DFS tree and therefore w is not in the subtree of v. Because v.lowlink takes into account nodes reachable only through the nodes in the subtree of v we must stop at w and use w.index instead of w.lowlink.
--------------------------------------------------------------------------------
9) __plot_graph(self) -> None -__ This function draws the graph with matplotlib lib.
    

### Output of image of scenario five(A5):

![](https://github.com/georgekouzi/DirectedWeightedGraph_onPython/blob/main/image/%E2%80%8F%E2%80%8F2.PNG?raw=true)

## explanation how its work : 
How It Works:
In the first step, a directed weighted graph must be created - For example:

 g = DiGraph()
graph.add_node(id key=0)-->key number 0
graph.add_node(id key=1)-->key number 1
graph.add_node(id key=2)-->key number 2
graph.add_node(id key=3)-->key number 3

    graph.add_edge(0, 1, 1)
    graph.add_edge(1, 0, 1.1)
    graph.add_edge(1, 2, 1.3)
    graph.add_edge(2, 3, 1.1)
    graph.add_edge(1, 3, 10)
    
now you can now use all the functions of the class DiGraph, For example:

    graph.get_all_v()  output-->     {0:0 , 1: 1: ,2: 2: ,3: 3}
    graph.all_in_edges_of_node(1) output--> {0: 1}
    graph.all_out_edges_of_node(1) output--> {0: 1.1, 2: 1.3, 3: 10}
    
At this point we will create Graph_Algo object :

    algo = Graph_Algo(graph).

now you can now use all the functions algoritem of the class, For example:
    
    algo.shortest_path(0, 3) output-->  (3.4, [0, 1, 2, 3])
    algo.connected_component(id=1) utput--> [0, 1]
    algo.connected_components()  output-->[[3], [2], [1, 0]]
    algo.save_to_json("../file//testGraph1").
    algo.load_from_json("../file//testGraph1").
    algo.plot_graph() output--> 
 
   ![](https://github.com/georgekouzi/DirectedWeightedGraph_onPython/blob/main/image/%E2%80%8F%E2%80%8F4.PNG?raw=20*20)



### The project was written by Dolev Saadia and George Kouzi:
--------
https://github.com/georgekouzi

--------

https://github.com/dolevsaadia

---------



