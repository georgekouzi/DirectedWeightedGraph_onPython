from src.GraphInterface import GraphInterface


class DiGraph(GraphInterface):

    def __init__(self):
        self.__graph={'node':{},'edge':{'from':{},'into':{}}}
        self.__mc=0
        self.__edgeSize=0
    def v_size(self) -> int:
        """
               Returns the number of vertices in this graph
               @return: The number of vertices in this graph
               """
        return self.__graph.get('node').__len__()


    def e_size(self) -> int:
        """
               Returns the number of edges in this graph
               @return: The number of edges in this graph
               """
        return self.__edgeSize



    def get_all_v(self) -> dict:
        """return a dictionary of all the nodes in the Graph, each node is represented using a pair  (key, node_data)
               """
        return self.__graph.get('node')


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
        if id1==id2 or weight<0:
            return False

        if not (self.__graph.get('node').__contains__(id1)) or not(self.__graph.get('node').__contains__(id2)):
            return False



        # graph.get('edge').get('from').update({1: {2: 1.2, 5: 0.23, 4: 1.33, 5: 1.34}, 2: {1: 32}})
        if self.__graph.get('edge').get('from').__contains__(id1):
            if not (self.__graph.get('edge').get('from').get(id1).__contains__(id2)):
                self.__graph.get('edge').get('from').get(id1).update({id2: weight})
                if self.__graph.get('edge').get('into').__contains__(id2):
                    self.__graph.get('edge').get('into').get(id2).update({id1: weight})
                else:
                    self.__graph.get('edge').get('into').update({id2:{id1: weight}})
                self.__edgeSize=self.__edgeSize+1
                self.__mc=self.__mc+1
                return True
            else:
                return False
        else:
            self.__graph.get('edge').get('from').update({id1:{id2: weight}})
            if self.__graph.get('edge').get('into').__contains__(id2):
                self.__graph.get('edge').get('into').get(id2).update({id1: weight})
            else:
                self.__graph.get('edge').get('into').update({id2: {id1: weight}})
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
        if not(self.__graph.get('node').__contains__(node_id)):
            self.__graph.get('node').update({node_id: pos})
            self.__mc=self.__mc+1
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
        if self.__graph.get('node').__contains__(node_id):
            del self.__graph['node'][node_id]
            self.__mc = self.__mc + 1

            if self.__graph.get('edge').get('from').__contains__(node_id):
                self.__mc=self.__mc+len(self.__graph.get('edge').get('from').get(node_id))
                self.__edgeSize=self.__edgeSize-len(self.__graph.get('edge').get('from').get(node_id))
                del self.__graph['edge']['from'][node_id]



            if self.__graph.get('edge').get('into').__contains__(node_id):
                for delEdge in self.__graph.get('edge').get('into').get(node_id):
                    del self.__graph['edge']['from'][delEdge][node_id]
                    self.__edgeSize = self.__edgeSize - 1
                    self.__mc = self.__mc + 1

                    if self.__graph['edge']['from'][delEdge] == {}:
                        del self.__graph['edge']['from'][delEdge]

                    if self.__graph.get('edge').get('into').__contains__(delEdge) and self.__graph.get('edge').get('into').get(delEdge).__contains__(node_id):
                        del self.__graph['edge']['into'][delEdge][node_id]

                        if self.__graph['edge']['into'][delEdge] == {}:
                            del self.__graph['edge']['into'][delEdge]

                del self.__graph['edge']['into'][node_id]
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
        if self.__graph.get('node').__contains__(node_id1) and self.__graph.get('node').__contains__(node_id2) and self.__graph.get('edge').get('from').__contains__(node_id1) and self.__graph.get('edge').get('from').get(node_id1).__contains__(node_id2):
            del self.__graph['edge']['from'][node_id1][node_id2]
            if  self.__graph['edge']['from'][node_id1]=={}:
                del self.__graph['edge']['from'][node_id1]
            del self.__graph['edge']['into'][node_id2][node_id1]
            if  self.__graph['edge']['into'][node_id2]=={}:
                del self.__graph['edge']['into'][node_id2]
            self.__edgeSize=self.__edgeSize+1
            self.__mc=self.__mc+1

            return True
        else:
            return False


graph1=DiGraph()
print(graph1.add_node(1,(1.23,1.34)))
print(graph1.add_node(2,(1.23,1.34)))
print(graph1.add_node(3,(1.23,1.34)))
print(graph1.get_all_v())
print("num of node=3",graph1.v_size())
print("num of edge=0",graph1.e_size())
print("num of mc=3",graph1.get_mc())
print(graph1.add_edge(1,2,1.33))
print(graph1.add_edge(1,3,1.33))
print(graph1.add_edge(2,1,1.33))
print(graph1.add_edge(3,1,1.33))
print("num of node=3",graph1.v_size())
print("num of edge=4",graph1.e_size())
print("num of mc=7",graph1.get_mc())
graph1.remove_node(1)
print("num of node=2",graph1.v_size())
print("num of edge=0",graph1.e_size())
print("num of mc=12",graph1.get_mc())

print(graph1.all_in_edges_of_node(1))
print(graph1.all_in_edges_of_node(2))
print(graph1.all_in_edges_of_node(3))
print(graph1.all_out_edges_of_node(1))
print(graph1.all_out_edges_of_node(2))
print(graph1.all_out_edges_of_node(3))
print(graph1.get_all_v())
graph1.remove_node(2)
print("num of node=1",graph1.v_size())
print("num of edge=0",graph1.e_size())
print("num of mc=13",graph1.get_mc())

print(graph1.all_in_edges_of_node(1))
print(graph1.all_in_edges_of_node(2))
print(graph1.all_in_edges_of_node(3))
print(graph1.all_out_edges_of_node(1))
print(graph1.all_out_edges_of_node(2))
print(graph1.all_out_edges_of_node(3))
print(graph1.get_all_v())
graph1.remove_node(3)
print("num of node=0",graph1.v_size())
print("num of edge=0",graph1.e_size())
print("num of mc=14",graph1.get_mc())

print(graph1.all_in_edges_of_node(1))
print(graph1.all_in_edges_of_node(2))
print(graph1.all_in_edges_of_node(3))
print(graph1.all_out_edges_of_node(1))
print(graph1.all_out_edges_of_node(2))
print(graph1.all_out_edges_of_node(3))
print(graph1.get_all_v())

# print(graph1.add_edge(1,1,1.33))
# print(graph1.add_edge(2,3,1.34))
# print(graph1.all_in_edges_of_node(1))
# print(graph1.all_out_edges_of_node(1))

# print(graph1.all_in_edges_of_node(2))
# print(graph1.all_out_edges_of_node(2))
#
#
#
# print(graph1.all_out_edges_of_node(3))
# print(graph1.all_in_edges_of_node(3))
#
# print(graph1.e_size())
#
# print("graph1.remove_edge(1,2)=",graph1.remove_edge(1,2))
# print("graph1.remove_edge(2,1)=",graph1.remove_edge(2,1))
# print("graph1.remove_edge(6,1)=",graph1.remove_edge(1,6))
#
# print(graph1.all_in_edges_of_node(1))
# print(graph1.all_in_edges_of_node(2))
#
# print(graph1.all_out_edges_of_node(1))
# print(graph1.all_out_edges_of_node(2))
# print(graph1.add_edge(1,2,1.344))
# print(graph1.all_in_edges_of_node(1))
# print(graph1.all_in_edges_of_node(2))
#
# print(graph1.all_out_edges_of_node(1))

