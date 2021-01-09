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


class GraphAlgo(GraphAlgoInterface):

    def __init__(self, graph=DiGraph()):

        self.__DWGraph = graph

    def get_graph(self) -> GraphInterface:
        """
        :return: the directed graph on which the algorithm works on.
        """
        return self.__DWGraph

    """
           Loads a graph from a json file.
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
                        self.__DWGraph.add_node(node.get("id"), (float(pos[0]), float(pos[1]), float(pos[2])))
                    else:
                        self.__DWGraph.add_node(node.get("id"))
                if "Edges" in DataGraph:
                    if DataGraph["Edges"] is not None or DataGraph["Edges"] is not {}:
                        for edge in DataGraph.get("Edges"):
                            self.__DWGraph.add_edge(edge.get("src"), edge.get("dest"), edge.get("w"))
            return True

        except FileExistsError:
            return False

    def save_to_json(self, file_name: str) -> bool:
        """
        Saves the graph in JSON format to a file
        @param file_name: The path to the out file
        @return: True if the save was successful, False o.w.
        """
        try:
            with open(file_name, "w") as ToJsonFile:
                all_node = self.__DWGraph.get_all_v()
                if all_node is None or all_node is {}:
                    return False
                new_graph = {"Nodes": [], "Edges": []}
                for node in all_node:

                    if all_node[node]["pos"] is None:
                        new_graph["Nodes"].append({"id": node})
                    else:
                        new_graph["Nodes"].append({"id": node,
                                                   "pos": str(all_node[node]["pos"][0]) + "," + str(
                                                       all_node[node]["pos"][1]) + "," + str(
                                                       all_node[node]["pos"][2])})

                    allEdge = self.__DWGraph.all_out_edges_of_node(node)
                    if allEdge is not None:
                        for edge in allEdge:
                            new_graph["Edges"].append({"src": node, "dest": edge, "w": allEdge[edge]})

                json.dump(new_graph, ToJsonFile)
                return True
        except FileExistsError:
            return False

    def shortest_path(self, id1: int, id2: int) -> (float, list):
        """
        Returns the shortest path from node id1 to node id2 using Dijkstra's Algorithm
        @param id1: The start node id
        @param id2: The end node id
        @return: The distance of the path, the path as a list

        Example:
#      >>> from GraphAlgo import GraphAlgo
#       >>> g_algo = GraphAlgo()
#        >>> g_algo.addNode(0)
#        >>> g_algo.addNode(1)
#        >>> g_algo.addNode(2)
#        >>> g_algo.addEdge(0,1,1)
#        >>> g_algo.addEdge(1,2,4)
#        >>> g_algo.shortestPath(0,1)
#        (1, [0, 1])
#        >>> g_algo.shortestPath(0,2)
#        (5, [0, 1, 2])

        More info:
        https://en.wikipedia.org/wiki/Dijkstra's_algorithm
        """

        if id1 not in self.__DWGraph.get_all_v() or id2 not in self.__DWGraph.get_all_v():
            return None, None

        if id1 == id2:
            return 0, [id1]

        myDict = self.__dijkstra(id1)
        if id2 not in myDict:
            return math.inf, None

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

    def __dijkstra(self, id_src):
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

    def connected_component(self, id1: int) -> list:
        """
        Finds the Strongly Connected Component(SCC) that node id1 is a part of.
        @param id1: The node id
        @return: The list of nodes in the SCC
        """
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

    def connected_components(self) -> List[list]:
        """
        Finds all the Strongly Connected Component(SCC) in the graph.
        @return: The list all SCC
        """
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

    def plot_graph(self) -> None:

        nodes = self.__DWGraph.get_all_v()
        for key in nodes:

            if nodes[key]["pos"] is None:
                x_pos = random.uniform(0, len(nodes))  # nodes[key][0]
                y_pos = random.uniform(0, len(nodes))  # nodes[key][1]
                nodes[key]["pos"] = (x_pos, y_pos, 0.0)

            else:
                x_pos = nodes[key]["pos"][0]
                y_pos = nodes[key]["pos"][1]

            edge = self.__DWGraph.all_out_edges_of_node(key)

            print_graph.scatter(x_pos, y_pos, color='r', zorder=1)
            print_graph.text(x_pos + 0.0001, y_pos + 0.0001, str(key), color='b', zorder=5, size=10)

            if edge is not None:

                for neighbor in edge:

                    if nodes[neighbor]["pos"] is None:
                        x_neighbor_pos = random.uniform(0, len(nodes))
                        y_neighbor_pos = random.uniform(0, len(nodes))
                        nodes[neighbor]["pos"] = (x_neighbor_pos, y_neighbor_pos, 0.0)

                    else:
                        x_neighbor_pos = nodes[neighbor]["pos"][0]
                        y_neighbor_pos = nodes[neighbor]["pos"][1]

                    print_graph.plot([x_pos, x_neighbor_pos], [y_pos, y_neighbor_pos], zorder=0, color='k')

                    u = np.diff([x_pos, x_neighbor_pos])
                    v = np.diff([y_pos, y_neighbor_pos])
                    arrow_x = x_pos + u * 0.8
                    arrow_y = y_pos + v * 0.8
                    print_graph.quiver(arrow_x, arrow_y, u, v, angles="xy", headwidth=2.5, zorder=0, pivot="mid",
                                       headlength=4, color='k', )

        print_graph.show()

    def __dfs(self, n, tarjan_dict):

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


# graph1=DiGraph()
# print(graph1.add_node(1,(1.23,1.34)))
# print(graph1.add_node(2,(1.23,1.34)))
# print(graph1.add_node(3,(1.23,1.34)))
# graphAlgo=GraphAlgo(graph1)
# # print(graphAlgo.load_from_json('A5'))
# print(graphAlgo.get_graph())
# # print(graphAlgo.save_to_json('kaka.txt'))
# # print(graphAlgo.load_from_json("A5"))
# # print(graphAlgo.get_graph())
# # print(graphAlgo.load_from_json("lama.txt"))
# node={1:{"dist":20,"vis":True,},2:{"dist":3,"vis":False}}
# # node.update({1:{"dist":20,"vis":True,},2:{"dist":3,"vis":False}})
# print(node.get(1))
# pQueue = PriorityQueue()
# NodeData={1:{"dist":0.0,"vis":True}}
# print(NodeData.get(1))
# NodeData.get(1).update({"dist":2222.32})
# print(NodeData.get(1))
# pQueue.put((43.2111,23))
# pQueue.put((3.11,22))
# pQueue.put((0.2,24))
# pQueue.put((0.3,25))
# while not pQueue.empty():
#
#     print(pQueue.get()[1])
# print(float(sys.maxsize))
# g = DiGraph()
# g.add_node(1)
# g.add_node(2)
# g.add_node(3)
# g.add_node(4)
# g.add_node(5)
# g.add_node(6)
# g.add_edge(1, 3, 9)
# g.add_edge(1, 2, 3.45)
# g.add_edge(1, 6, 14)
# g.add_edge(2, 3, 10)
# g.add_edge(2, 4, 2.34322)
# g.add_edge(3, 6, 2)
# g.add_edge(3, 4, 11)
# g.add_edge(4, 5, 6)
# g.add_edge(6, 5, 9)
# g.add_edge(5, 3, 2.1211)
# g.add_edge(4, 2, 2.34322)
# g.add_edge(2, 1, 3.45)
# algo = GraphAlgo(g)
# print(algo.get_graph())
# print(algo.shortest_path(1, 5))
# print(algo.connected_components())
# g = DiGraph()
# g.add_node(0)
# g.add_node(1)
# g.add_node(2)
# g.add_edge(2, 0, 0)
# g.add_edge(2, 1, 0)
# g.add_edge(0, 1, 0)
# g.add_edge(1, 0, 0)
# algo = GraphAlgo(g)
# print(algo.connected_components())
# print(algo.connected_component(0))
# print(algo.load_from_json("A5"))
# print(algo.connected_components())
g = DiGraph()
g.add_node(0)
g.add_node(1)
g.add_node(2)
g.add_node(3)
g.add_node(4)
g.add_node(5)

g.add_edge(0, 1, 0)
g.add_edge(1, 2, 0)
g.add_edge(2, 3, 0)
# g.add_edge(3, 0, 0)
g.add_edge(3, 4, 0)
g.add_edge(4, 3, 0)
algo = GraphAlgo(g)
# print(algo.connected_components())
# print(algo.connected_component(6))
# algo.plot_graph()
# algo.load_from_json("T0.json_saved")
# print(algo.get_graph())
# algo.plot_graph()
# a = np.linspace(-2,2, 100)
# print(a)
# # print_graph.plot(a, a**2)
# print_graph.annotate("here", xy=(0, 0), xytext=(0, 2), arrowprops=dict(arrowstyle="->"))
# print_graph.show()
# x=[0,3,8,7,5,3,2,1]
# y=[0,1,3,5,9,8,7,5]
# print("x = ",[0,3,8,7,5,3,2,1])
# print("y = ",[0,1,3,5,9,8,7,5])
# print("a[i+1]-a[i]")

# u = np.diff(x)
# v = np.diff(y)
# print("u = np.diff(x)=",u)
# print("v = np.diff(y) = ",v)
#
# pos_x = x[:-1] + u*0.9
# print("x[:-1]= ",x[:-1],"u/2= ",u/2)
# pos_y = y[:-1] + v*0.9
# print("y[:-1]= ",y[:-1],"v/2= ",v/2)
# print("pos_x = x[:-1] + u/2=",pos_x)
# print("pos_y = y[:-1] + v/2 = " ,pos_y)
# norm = np.sqrt(u**2+v**2)
# print("norm = np.sqrt(u**2+v**2) = ",norm)

# fig, ax = print_graph.subplots()
# print_graph.plot(x,y,marker="o")
# print_graph.quiver(pos_x, pos_y, u, v, angles="xy", zorder=5, pivot="mid")
# print_graph.show()

# algo.load_from_json('A5')
# algo.plot_graph()
# nodes=algo.get_graph().get_all_v()
# print(nodes)
# nodes.values()
# x=[]
# y=[]
# for key in nodes:
#     x_pos=nodes[key][0]
#     y_pos=nodes[key][1]
#     x.append(x_pos)
#     y.append(y_pos)
#     print_graph.scatter(x_pos,y_pos,color='r')
#     print_graph.text(x_pos+0.0001,y_pos+0.0001,str(key),color='g',zorder=100)
# # print(x_pos)
# # print(y_pos)
#     edge=algo.get_graph().all_out_edges_of_node(key)
#     for neighbor in edge:
#         x_neighbor_pos=nodes[neighbor][0]
#         y_neighbor_pos=nodes[neighbor][1]
#         x.append(x_neighbor_pos)
#         y.append(y_neighbor_pos)
#         # print_graph.scatter([x_pos,x_neighbor_pos],[y_pos,y_neighbor_pos],color='r')
# u = np.diff(x)
# v = np.diff(y)
# arrow_x = x[:-1]+u*0.8
# arrow_y = y[:-1]+v*0.8
#
# # fig, ax = print_graph.subplots()
# # print_graph.scatter(x,y,color='r')
# print_graph.plot(x,y,color='k')
# print_graph.quiver(arrow_x,arrow_y, u, v, angles="xy", zorder=5, pivot="mid",color='k')
# # ax.show()
#
# #
# #
# #
# #
# # print_graph.show()
# g = DiGraph()
# g.add_node(1)
# g.add_node(2)
# g.add_node(3)
# g.add_edge(1, 3, 0)
#
# algo = GraphAlgo(g)
# algo.plot_graph()

# st = [4]
# print(st[len(st) - 1])
# print(None)
