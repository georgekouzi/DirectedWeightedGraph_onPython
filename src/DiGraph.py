from src.GraphInterface import GraphInterface
from src.Node import Node


class DiGraph(GraphInterface):

    def __init__(self):
        self.__graph = {'node': {}, 'edge': {'from': {}, 'into': {}}}
        self.__mc = 0
        self.__edgeSize = 0

    def v_size(self) -> int:
        """
               Returns the number of vertices in this graph
               @return: The number of vertices in this graph
               """
        return len(self.__graph.get('node'))

    def e_size(self) -> int:
        """
               Returns the number of edges in this graph
               @return: The number of edges in this graph
               """
        return self.__edgeSize

    def get_all_v(self) -> dict:
        """return a dictionary of all the nodes in the Graph, each node is represented using a pair  (key, node_data)
               """
        return self.__graph.get("node")

    def all_in_edges_of_node(self, id1: int) -> dict:
        """return a dictionary of all the nodes connected to (into) node_id,
               each node is represented using a pair (key, weight)
                """
        return self.__graph.get('edge').get('into').get(id1)

    def all_out_edges_of_node(self, id1: int) -> dict:
        """return a dictionary of all the nodes connected from node_id ,
         each node is represented using a pair (key,weight)
         """
        return self.__graph.get('edge').get('from').get(id1)

    def get_mc(self) -> int:
        """
              Returns the current version of this graph,
              on every change in the graph state - the MC should be increased
              @return: The current version of this graph.
              """
        return self.__mc

    def add_edge(self, id1: int, id2: int, weight: float) -> bool:
        """
        Adds an edge to the graph.
        @param id1: The start node of the edge
        @param id2: The end node of the edge
        @param weight: The weight of the edge
        @return: True if the edge was added successfully, False o.w.

        Note: If the edge already exists or one of the nodes dose not exists the functions will do nothing
        """
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

    def add_node(self, node_id: int, pos: tuple = None) -> bool:
        """
               Adds a node to the graph.
               @param node_id: The node ID
               @param pos: The position of the node
               @return: True if the node was added successfully, False o.w.

               Note: if the node id already exists the node will not be added
               """
        if node_id not in self.__graph.get('node') and node_id >= 0:
            self.__graph.get('node').update({node_id: Node(node_id, pos)})
            self.__mc = self.__mc + 1
            return True
        else:
            return False

    def remove_node(self, node_id: int) -> bool:
        """
        Removes a node from the graph.
        @param node_id: The node ID
        @return: True if the node was removed successfully, False o.w.

        Note: if the node id does not exists the function will do nothing
        """

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

    def remove_edge(self, node_id1: int, node_id2: int) -> bool:
        """
        Removes an edge from the graph.
        @param node_id1: The start node of the edge
        @param node_id2: The end node of the edge
        @return: True if the edge was removed successfully, False o.w.

        Note: If such an edge does not exists the function will do nothing
        """
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




