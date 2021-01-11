import json
import timeit
import networkx as nx
import matplotlib.pyplot as plt


def load_networkx_from_json(file_name: str) :
    try:

        with open(file_name, 'r') as JsonFile:

            DataGraph = json.load(JsonFile)
            newGraph = nx.DiGraph()

            if 'Nodes' in DataGraph or DataGraph["Nodes"]:

                for node in DataGraph.get("Nodes"):

                    if "pos" in node:
                        pos = node.get("pos").split(",")
                        newGraph.add_node(node["id"], pos=(float(pos[0]), float(pos[1])))
                    else:
                        newGraph.add_node(node.get("id"))

            if "Edges" in DataGraph:
                if DataGraph["Edges"] is not None:

                    for edge in DataGraph.get("Edges"):
                        newGraph.add_edge(edge.get("src"), edge.get("dest"), weight=edge.get("w"))

        return newGraph

    except FileExistsError:
        return None


# def save_to_json(self, file_name: str) -> bool:


def run_time(file_name: str, src: int, dest: int):
    dt = 0
    for i in range(100):
        start = timeit.default_timer()
        graph_networkx = load_networkx_from_json(file_name)
        stop = timeit.default_timer()
        dt = dt + (stop - start)

    print("Graph: |V|=", graph_networkx.number_of_nodes(), " , |E|=", graph_networkx.number_of_edges())
    print("run time of read from json file and build the graph: ", dt / 100)

    dt = 0
    for i in range(100):
        start = timeit.default_timer()
        connected_components = []
        for c in nx.strongly_connected_components(graph_networkx):
            connected_components.append(c)
        stop = timeit.default_timer()

        dt = dt + (stop - start)

    print("run time of connected_component: ", dt / 100)

    dt = 0
    for i in range(100):
        start = timeit.default_timer()
        short = nx.dijkstra_path(graph_networkx, src, dest, weight='weight')
        # print((short))
        stop = timeit.default_timer()
        dt = dt + (stop - start)

    print("run time of shortest_path: ", dt / 100)

    # dt = 0
    # for i in range(100):
    #     start = timeit.default_timer()
    #     pos = nx.get_node_attributes(graph_networkx, 'pos')
    #
    #     if pos != {}:
    #         nx.draw_networkx(graph_networkx, nx.get_node_attributes(graph_networkx,'pos'),node_size=80,arrowsize=5,width=1.0,with_labels=True)
    #     else:
    #         pos=nx.random_layout(graph_networkx)
    #         nx.draw_networkx(graph_networkx,pos,node_size=80,arrowsize=5,width=1.0,with_labels=True)
    #
    #     plt.show()
    #     stop = timeit.default_timer()
    #     dt = dt + (stop - start)
    #
    # print("run time of plot graph: ", dt/100)
    print()


if __name__ == '__main__':
    run_time('../data/G_10_80_1.json', 0, 9)
    run_time('../data/G_100_800_1.json', 0, 99)
    run_time('../data/G_1000_8000_1.json', 0, 999)
    run_time('../data/G_10000_80000_1.json', 0, 9999)
    run_time('../data/G_20000_160000_1.json', 0, 19999)
    run_time('../data/G_30000_240000_1.json', 0, 29999)
