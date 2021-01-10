import timeit
from src.GraphAlgo import GraphAlgo




def run_time(file_name:str,src,dest):
    graph_algo = GraphAlgo()
    dt=0
    for i in range(100):
        start = timeit.default_timer()
        graph_algo.load_from_json(file_name)
        stop = timeit.default_timer()
        dt = dt+(stop-start)
    print(graph_algo.get_graph())
    print("run time of read from json file and build the graph: ", dt/100)
    dt = 0
    for i in range(100):
        start = timeit.default_timer()
        connecteds = graph_algo.connected_components()
        stop = timeit.default_timer()
        dt = dt+(stop-start)
        # print(connecteds)
    print("run time of connected_components: ", dt/100)

    dt = 0
    for i in range(100):
        start = timeit.default_timer()
        graph_algo.connected_component(1)
        stop = timeit.default_timer()
        dt = dt+(stop-start)

    print("run time of connected_component: ", dt/100)

    dt = 0
    for i in range(100):
        start = timeit.default_timer()
        graph_algo.shortest_path(src, dest)
        stop = timeit.default_timer()
        dt = dt+(stop-start)
    print("run time of shortest_path: ", dt/100)

    # dt = 0
    # for i in range(100):
    #     start = timeit.default_timer()
    #     graph_algo.plot_graph()
    #     stop = timeit.default_timer()
    # print("run time of plot graph: ", dt/100)
    # print()






if __name__ == '__main__':
    run_time('../data/G_10_80_1.json', 0, 9)
    run_time('../data/G_100_800_1.json', 0, 99)
    run_time('../data/G_1000_8000_1.json', 0, 999)
    run_time('../data/G_10000_80000_1.json', 0, 9999)
    run_time('../data/G_20000_160000_1.json', 0, 19999)
    run_time('../data/G_30000_240000_1.json', 0, 29999)


