import json
from queue import PriorityQueue
import sys
from src.DiGraph import DiGraph
from src.GraphAlgoInterface import GraphAlgoInterface
from typing import List
from src import GraphInterface
import numpy as np
import matplotlib.pyplot as print_graph
import random
import math
from src.Node import Node
"""
 This class knows how to do operations on graphs.
 We can check scc on  the graph and know if it Strongly Connected, check the cheap path between two nodes and the cheap distance between two nodes.
 We can save the graph on json file and load the graph from json file.
 This class uses a DFS algorithm that allows running on all nodes in the graph and do transpoz to the graph edge in run time O(n+m).
 This class uses a Dijkstra algorithm that allows running on all nodes in the graph and find the cheap path two nodes in run time O(E*log(V)).
 https://en.wikipedia.org/wiki/Tarjan%27s_strongly_connected_components_algorithm.
 https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm.
 @author George kouzy and Dolev Saadia. 
"""
class GraphAlgo(GraphAlgoInterface):

    def __init__(self, graph=DiGraph()):

        self.__DWGraph = graph
    """
    This function return your graph.
    @reterns this graph.
    """
    def get_graph(self) -> GraphInterface:

        return self.__DWGraph

    """
    Load this json file (directed weighted graph). This function path of json file name on the computer. 
    The default path to this file is in the project folder. 
    we use json lib- Which allows us to extract the information from the json file that we need and read it 
    and create a new graph . and its data can be used to recreate the object in memory. The information we want to 
    load is: a dictionary of list of all edges and list of all nodes. the run time is: O(E*V)- E - edges and V-nodes. 
    we use json folder to get json file load.           
    @param file_name: The path to the json file
    @returns True if the loading was successful, False o.w.
    """

    def load_from_json(self, file_name: str) -> bool:

        try:
            with open(file_name, 'r') as JsonFile:

                self.__DWGraph = DiGraph()
                DataGraph = json.load(JsonFile)

                if 'Nodes' not in DataGraph or DataGraph["Nodes"] is None or DataGraph["Nodes"] is {}:
                    return False

                for node in DataGraph.get("Nodes"):
                    if "pos" in node:
                        pos = node.get("pos").split(",")
                        self.__DWGraph.add_node(node.get("id"),(float(pos[0]), float(pos[1]), float(pos[2])))
                    else:
                        self.__DWGraph.add_node(node.get("id"))
                if "Edges" in DataGraph:
                    if DataGraph["Edges"] is not None or DataGraph["Edges"] is not {}:
                        for edge in DataGraph.get("Edges"):
                            self.__DWGraph.add_edge(edge.get("src"), edge.get("dest"), edge.get("w"))
            return True

        except FileExistsError:
            return False

    """
    Saves this directed weighted graph to this json file name(file_name:str).
    This function path of json file name on the computer.
    The default path to this file is in the project folder(src).
    we use json lib- Which allows us to extract the information we need and write it into the json file. T
    he information we want to keep is: dictionary of list of all the edges and list of all the nodes.
    @param file_name: The path to the out file
    @return: True if the save was successful, False o.w.
    """

    def save_to_json(self, file_name: str) -> bool:

        try:
            with open(file_name, "w") as ToJsonFile:
                all_node = self.__DWGraph.get_all_v()
                if all_node is None or all_node is {}:
                    return False
                new_graph = {"Nodes": [], "Edges": []}
                for node in all_node:

                    if all_node[node].get_pos() is None:
                        new_graph["Nodes"].append({"id": node})
                    else:
                        new_graph["Nodes"].append({"id": node,
                                                   "pos": str(all_node[node].get_pos()[0]) + "," + str(
                                                       all_node[node].get_pos()[1]) + "," + str(
                                                       all_node[node].get_pos()[2])})

                    allEdge = self.__DWGraph.all_out_edges_of_node(node)
                    if allEdge is not None:
                        for edge in allEdge:
                            new_graph["Edges"].append({"src": node, "dest": edge, "w": allEdge[edge]})

                json.dump(new_graph, ToJsonFile)
                return True
        except FileExistsError:
            return False




    """
    This function returns tuple of the length of the shortest path between src to dest and the shortest pat list between src to dest - as an ordered List of nodes: source--> n1-->n2-->...destination. 
    In order to find the shortest path from source node to destination node we will use the algorithm of dijkstra.. if src==dest we return (inf, [id1])
    or if no path between the node -->  we return (inf, None).
    @param id1: The start node id
    @param id2: The end node id
    @return: The distance of the path, the path as a list
    """


    def shortest_path(self, id1: int, id2: int) -> (float, list):


        if id1 not in self.__DWGraph.get_all_v() or id2 not in self.__DWGraph.get_all_v():
            return None, []

        if id1 == id2:
            return 0, [id1]

        myDict = self.__dijkstra(id1)
        if id2 not in myDict:
            return math.inf, []

        parents = myDict.get(id2).get("parents")
        if parents == -1:
            return math.inf, None

        myPath = [id2]
        while parents != id1:
            myPath.append(parents)
            parents = myDict.get(parents).get("parents")

        myPath.append(id1)
        myPath.reverse()

        return myDict.get(id2).get("dist"), myPath
    """
         This algorithm makes it possible to go over a weighted directed graph And find the cheapest ways from the 
         source node to the rest of the graph nodes. 
         The weights in the graph symbolize distance. 
         The shortest route between two points means the route with the lowest amount of weights between the two vertices. 
         we use inner class that call nodeAlgo to save all the data that dijkstra algorithm need. 
         Ran time- O(E*log(V)) because we create PriorityQueue and compare the node by the minimum distance .
         @returns - dictionary of all the node with information about the chipsets paths from the source node 
         to all the node in the graph  
         for More info:
         https://en.wikipedia.org/wiki/Dijkstra's_algorithm
    """

    def __dijkstra(self, id_src)->dict:
        pQueue = PriorityQueue()
        node_data = {id_src: {"dist": 0.0, "vis": False, "parents": -1}}
        pQueue.put((node_data.get(id_src).get("dist"), id_src))
        while not pQueue.empty():
            n = pQueue.get()[1]
            neighbor_w = self.__DWGraph.all_out_edges_of_node(n)

            if neighbor_w is not None:
                for neighbor in neighbor_w:

                    if neighbor not in node_data:
                        node_data.update({neighbor: {"dist": sys.maxsize, "vis": False, "pereants": -1}})

                    if not node_data.get(neighbor).get("vis"):
                        newDist = node_data.get(n).get("dist") + neighbor_w[neighbor]
                        if node_data.get(neighbor).get("dist") > newDist:
                            node_data.get(neighbor).update({"dist": newDist})
                            pQueue.put((node_data.get(neighbor).get("dist"), neighbor))
                            node_data.get(neighbor).update({"parents": n})

                    node_data.get(n).update({"vis": True})

        return node_data
    """
    This function checks if there is a Circular  Path from node id1 node to all the nodes With Dfs Algorithm- 
    this is an improved DFS called Tarjan Algorithm. after use DFS Algorithm we get list of list of all the phath in this component. 
    Tarjan_Algo dictionary - serves data Structure: stack ,lowlink ,count and st_trace. 
    run time O(E + V): E- the number of ribs, V- the number of nodes.
    @param id1: The node id
    @return: The list of nodes in the SCC
    """
    def connected_component(self, id1: int) -> list:

        if self.__DWGraph.get_all_v() is None or id1 not in self.__DWGraph.get_all_v():
            return []

        tarjan_dict = {"Nodes": {}, "count": 0, "stack": [], "st_trace": [], "component": []}
        tarjan_dict.get("Nodes").update({id1: {"low_link": 0, "vis": -1}})

        tarjan_dict = self.__dfs(id1, tarjan_dict)

        ConnectedNodes = tarjan_dict.get("component")
        length = len(ConnectedNodes)

        if length == 1:
            return ConnectedNodes[0]

        else:
            for findId1 in ConnectedNodes:
                if id1 in findId1:
                    ConnectedNodes = findId1
                    break

        return ConnectedNodes
    """
    This function checks if there is a Path from each node to all the nodes With Dfs Algorithm- 
    this is an improved DFS called Tarjan Algorithm. 
    after use DFS Algorithm we get list of list of all the phath in this component  if the size of the list  
    equal to 1 So the graph is strongly connected and can be reached from any node to any other node. 
    Tarjan_Algo dictionary - serves data Structure: stack ,lowlink ,count and st_trace. 
    run time O(E + V): E- the number of ribs, V- the number of nodes.
    @return: The list all SCC
    """

    def connected_components(self) -> List[list]:

        if self.__DWGraph.get_all_v() is None:
            return []

        component = []
        tarjan_dict = {"Nodes": {}, "count": 0, "stack": [], "st_trace": [], "component": []}
        for node in self.__DWGraph.get_all_v():

            if node not in tarjan_dict.get("Nodes"):
                tarjan_dict.get("Nodes").update({node: {"low_link": 0, "vis": -1}})

            if tarjan_dict.get("Nodes").get(node)["vis"] == -1:
                tarjan_dict = self.__dfs(node, tarjan_dict)

            component = tarjan_dict.get("component")

        return component
    """
    This function draws the graph with matplotlib lib.
    """
    def plot_graph(self) -> None:

        nodes = self.__DWGraph.get_all_v()

        for key in nodes:

            if nodes[key].get_pos() is None:
                x_pos = random.uniform(0, len(nodes))
                y_pos = random.uniform(0, len(nodes))
                nodes[key].set_pos( (x_pos, y_pos, 0.0))

            else:
                x_pos = nodes[key].get_pos()[0]
                y_pos = nodes[key].get_pos()[1]

            edge = self.__DWGraph.all_out_edges_of_node(key)

            print_graph.scatter(x_pos, y_pos, color='r', zorder=1)
            print_graph.text(x_pos + 0.0001, y_pos + 0.0001, str(key), color='b', zorder=5, size=10)

            if edge is not None:

                for neighbor in edge:

                    if nodes[neighbor].get_pos() is None:

                        x_neighbor_pos = random.uniform(0, len(nodes))
                        y_neighbor_pos = random.uniform(0, len(nodes))
                        nodes[neighbor].set_pos ((x_neighbor_pos, y_neighbor_pos, 0.0))

                    else:
                        x_neighbor_pos = nodes[neighbor].get_pos()[0]
                        y_neighbor_pos = nodes[neighbor].get_pos()[1]

                    print_graph.plot([x_pos, x_neighbor_pos], [y_pos, y_neighbor_pos], zorder=0, color='k')

                    # find all the point on this line
                    u = np.diff([x_pos, x_neighbor_pos])
                    v = np.diff([y_pos, y_neighbor_pos])
                    arrow_x = x_pos + u * 0.8
                    arrow_y = y_pos + v * 0.8
                    print_graph.quiver(arrow_x, arrow_y, u, v, angles="xy", headwidth=2.5, zorder=0, pivot="mid",
                                       headlength=4, color='k', )

        print_graph.show()
        return None
    """
     his algorithm makes it possible to go over a weighted directed graph the node stack, 
     which starts out empty and stores the history of nodes explored but not yet committed to a strongly connected component.
     as nodes are not popped as the search returns up the tree; 
     they are only popped when an entire strongly connected component has been found. 
     The outermost loop searches each node that has not yet been visited, ensuring that nodes which are not reachable 
     from the first node are still eventually traversed. 
     finding all successors from the node v, and reporting all strongly connected components of that subgraph. 
     When each node finishes recursing, if its lowlink is still set to its index, 
     then it is the root node of a strongly connected component, formed by all of the nodes above it on the stack. 
     The algorithm pops the stack up to and including the current node, and presents all of these nodes as a strongly connected component. 
     Note that v.lowlink := min(v.lowlink, w.index) is the correct way to update v.lowlink if w is on stack. 
     Because w is on the stack already, (v, w) is a back-edge in the DFS tree and therefore w is not in the subtree of v. 
     Because v.lowlink takes into account nodes reachable only through the nodes in the subtree of v we must stop at w 
     and use w.index instead of w.lowlink.
     @returns - dictionary of all scc 

    """

    def __dfs(self, n, tarjan_dict)->dict:

        parent = {}
        parent.update({n: n})
        tarjan_dict.get("stack").append(n)

        while len(tarjan_dict.get("stack")) != 0:

            n = tarjan_dict.get("stack")[len(tarjan_dict.get("stack")) - 1]
            if tarjan_dict.get("Nodes").get(n).get("vis") == -1:
                tarjan_dict.get("st_trace").append(n)

                tarjan_dict.get("Nodes").get(n).update({"low_link": tarjan_dict.get("count")})
                tarjan_dict.get("Nodes").get(n).update({"vis": tarjan_dict.get("count")})
                tarjan_dict.update({"count": tarjan_dict.get("count") + 1})

            flag = True
            edge_of_node = self.__DWGraph.all_out_edges_of_node(n)

            if edge_of_node is not None:

                for edge in edge_of_node:

                    if edge not in tarjan_dict.get("Nodes"):
                        tarjan_dict.get("Nodes").update({edge: {"low_link": 0, "vis": -1}})



                    if tarjan_dict.get("Nodes").get(edge).get("vis") == -1:
                        flag = False
                        parent.update({edge: n})
                        tarjan_dict.get("stack").append(edge)
                        break

                    elif tarjan_dict.get("Nodes").get(edge).get("low_link") < tarjan_dict.get("Nodes").get(n).get(
                            "low_link"):
                        tarjan_dict.get("Nodes").get(n).update(
                            {"low_link": tarjan_dict.get("Nodes").get(edge).get("low_link")})
            if flag:
                n = tarjan_dict.get("stack").pop()
                if tarjan_dict.get("Nodes").get(n)["low_link"] < tarjan_dict.get("Nodes").get(parent.get(n))[
                    "low_link"]:
                    tarjan_dict.get("Nodes").get(parent.get(n)).update(
                        {"low_link": tarjan_dict.get("Nodes").get(n).get("low_link")})
                if tarjan_dict.get("Nodes").get(n).get("low_link") == tarjan_dict.get("Nodes").get(n).get("vis"):

                    tr_stack = tarjan_dict.get("st_trace")
                    component = []
                    while True:
                        my_node = tr_stack.pop()

                        component.append(my_node)
                        tarjan_dict.get("Nodes").get(my_node).update({"low_link": sys.maxsize})

                        if my_node == n:
                            break

                    tarjan_dict.get("component").append(component)

        return tarjan_dict


