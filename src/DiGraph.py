from src.GraphInterface import GraphInterface
from src.Node import Node

"""
 This class creates an directed weighted graph that holds the addition of nodes
  You can add new nodes, connect two nodes by ribs, delete nodes, delete ribs between two nodes, 
  you can get the list of all the neighbors of a particular node and list of all the nodes.
  In addition, you can know the number of nodes in the graph, the number of ribs 
  and the number of actions performed in the graph (such as deleting the addition of a node)
  @author George kouzy and Dolev Saadia. 
"""


class DiGraph(GraphInterface):

    def __init__(self):
        self.__graph = {'node': {}, 'edge': {'from': {}, 'into': {}}}
        self.__mc = 0
        self.__edgeSize = 0

    """
    This function returns the amount of the nodes that exist in the graph.
     @return: The number of vertices in this graph
 
    """

    def v_size(self) -> int:

        return len(self.__graph.get('node'))

    """
    This function returns the amount of the edges that exist in the graph.
    @return: The number of edges in this graph
    """

    def e_size(self) -> int:

        return self.__edgeSize

    """
    This function return a dictionary of all the nodes in the graph.

    """

    def get_all_v(self) -> dict:

        return self.__graph.get("node")

    """
    This function return a dictionary of all the nodes connected to (into) node_id. 
    the function gets a source node key and returns all the parents node that connect to this id1 node. 
    If there are no parents nodes that connect to this node or this node does not exist at all the function will 
    return an empty dictionary,the dictionary output need see like that:
    {0: 1.1, 2: 1.3, 3: 10} - dictionary of key(the parents node) and value( weighted of the edge- destination 
    node(id1) <------- all the source node.
    """

    def all_in_edges_of_node(self, id1: int) -> dict:

        if id1 in self.__graph['node'] and id1 in self.__graph['edge']['into']:
            return self.__graph.get('edge').get('into').get(id1)
        else:
            return {}

    """
    This function return a dictionary of all the nodes connected to (from) node_id. 
    the function gets a source node key and returns all the neighbors node that connect to this id1 node. 
    If there are no neighbors nodes that connect to this node or this node does not exist at all the function will 
    return an empty dictionary,the dictionary output need see like that:
    {0: 1.1, 2: 1.3, 3: 10} - dictionary of key(the neighbors node) and value( weighted of the 
    edge- source node(id1) ------> destination node .
    """

    def all_out_edges_of_node(self, id1: int) -> dict:

        if id1 in self.__graph['node'] and id1 in self.__graph['edge']['from']:
            return self.__graph.get('edge').get('from').get(id1)

    """
    This function returns to the amount of operations that we did in the graph.
    @return: The current version of this graph.

    """

    def get_mc(self) -> int:

        return self.__mc

    """
     This function receives a Key of source node (id1), key of destination(id2) node and weight(weight) of the new edge.
     and creat a new edge and adds it to the graph dictionary and update the mode Count(mc) and finally return true . 
     if the edge already exists the function will do nothing and return false. 
     this function also checks if the weight is positive (i.e. does not allow insertion of negative weight.
     @param id1: The start node of the edge
     @param id2: The end node of the edge
     @param weight: The weight of the edge
     @return: True if the edge was added successfully, False o.w.
    """

    def add_edge(self, id1: int, id2: int, weight: float) -> bool:

        if id1 == id2 or weight < 0:
            return False

        if id1 not in self.__graph.get('node') or id2 not in self.__graph.get('node'):
            return False

        if id1 in self.__graph.get('edge').get('from'):
            if id2 not in self.__graph.get('edge').get('from').get(id1):
                self.__graph.get('edge').get('from').get(id1).update({id2: weight})
                if id2 in self.__graph.get('edge').get('into'):
                    self.__graph.get('edge').get('into').get(id2).update({id1: weight})
                else:
                    self.__graph.get('edge').get('into').update({id2: {id1: weight}})

                self.__graph["node"][id1].c_edge_out()
                self.__graph["node"][id2].c_edge_in()
                self.__edgeSize = self.__edgeSize + 1
                self.__mc = self.__mc + 1
                return True
            else:
                return False
        else:
            self.__graph.get('edge').get('from').update({id1: {id2: weight}})
            if id2 in self.__graph.get('edge').get('into'):
                self.__graph.get('edge').get('into').get(id2).update({id1: weight})
            else:
                self.__graph.get('edge').get('into').update({id2: {id1: weight}})

            self.__graph["node"][id1].c_edge_out()
            self.__graph["node"][id2].c_edge_in()
            self.__edgeSize = self.__edgeSize + 1
            self.__mc = self.__mc + 1
            return True

    """
    This function receives a new node and adds it to the _graph dictionary and update the mode Count(mc) 
    and finally return true. 
    If the node already exists in the graph dictionary nothing will be done and the function return false.
    @param node_id: The node ID
    @param pos: The position of the node
    @return: True if the node was added successfully, False o.w.

    """

    def add_node(self, node_id: int, pos: tuple = None) -> bool:

        if node_id not in self.__graph.get('node') and node_id >= 0:
            self.__graph.get('node').update({node_id: Node(node_id, pos)})
            self.__mc = self.__mc + 1
            return True
        else:
            return False

    """
    This function receives a key of a particular node and deletes it from the graph. This function searches for all the edges that have this destination node node_id and all the edges that have this sorce node (node_id) . Finally it will delete the node from the _graph dictionary and retune true . 
    If this node does not exist the function will return false.
    @param node_id: The node ID
    @return: True if the node was removed successfully, False o.w.
 
    """

    def remove_node(self, node_id: int) -> bool:

        if node_id in self.__graph.get('node'):

            if node_id in self.__graph.get('edge').get('from'):
                for delEdge in self.__graph.get('edge').get('from')[node_id]:
                    self.get_all_v()[delEdge].c_edge_in(-1)
                    del self.__graph['edge']['into'][delEdge][node_id]
                    self.__edgeSize = self.__edgeSize - 1
                    self.__mc = self.__mc + 1
                    if self.__graph['edge']['into'][delEdge] == {}:
                        del self.__graph['edge']['into'][delEdge]

                del self.__graph['edge']['from'][node_id]

            if node_id in self.__graph.get('edge').get('into'):
                for delEdge in self.__graph.get('edge').get('into')[node_id]:
                    self.get_all_v()[delEdge].c_edge_out(-1)
                    del self.__graph['edge']['from'][delEdge][node_id]
                    self.__edgeSize = self.__edgeSize - 1
                    self.__mc = self.__mc + 1

                    if self.__graph['edge']['from'][delEdge] == {}:
                        del self.__graph['edge']['from'][delEdge]

                del self.__graph['edge']['into'][node_id]

            del self.__graph['node'][node_id]
            self.__mc = self.__mc + 1

            return True
        else:
            return False

    """
    This function gets two keys, a source node_id1 and a destination node_id2, the function checks if this edge exists and deletes this edge and returns true. 
    If the edge does not exist the function returns false.
    @param node_id1: The start node of the edge
    @param node_id2: The end node of the edge
    @return: True if the edge was removed successfully, False o.w.

    """

    def remove_edge(self, node_id1: int, node_id2: int) -> bool:

        if node_id1 in self.__graph.get('node') and node_id2 in self.__graph.get(
                'node') and node_id1 in self.__graph.get('edge').get('from') and node_id2 in self.__graph.get(
            'edge').get('from').get(node_id1):

            self.get_all_v()[node_id1].c_edge_out(-1)
            del self.__graph['edge']['from'][node_id1][node_id2]
            if self.__graph['edge']['from'][node_id1] == {}:
                del self.__graph['edge']['from'][node_id1]

            self.get_all_v()[node_id2].c_edge_in(-1)
            del self.__graph['edge']['into'][node_id2][node_id1]
            if self.__graph['edge']['into'][node_id2] == {}:
                del self.__graph['edge']['into'][node_id2]

            self.__edgeSize = self.__edgeSize - 1
            self.__mc = self.__mc + 1

            return True
        else:
            return False

    def __repr__(self):
        return "Graph: |V|=" + str(self.v_size()) + " , |E|=" + str(self.e_size())

    def __str__(self):
        return "Graph: " + "|V|=" + str(self.v_size()) + " , |E|=" + str(self.e_size())

    def __eq__(self, other):
        if self.__graph == other.__graph:
            return True
        else:
            return False
