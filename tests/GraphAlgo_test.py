import random
import unittest
import math
from src.DiGraph import DiGraph
from src.GraphAlgo import GraphAlgo


class GraphAlgoTestCase(unittest.TestCase):

    def test_empty_graph(self):
        graph = DiGraph()
        graph_algo = GraphAlgo(graph)
        self.assertEqual(graph.v_size(), 0)
        self.assertEqual(graph.e_size(), 0)
        self.assertEqual(graph_algo.shortest_path(0, 0), (None, []))
        self.assertEqual(graph_algo.connected_component(1), [])
        self.assertEqual(graph_algo.connected_components(), [])
        self.assertTrue(graph_algo.save_to_json('../data/empty_graph'))
        self.assertTrue((graph_algo.load_from_json('../data/empty_graph')))
        self.assertEqual(graph_algo.get_graph().v_size(), 0)
        self.assertEqual(graph_algo.get_graph().e_size(), 0)

    def test_one_node_graph(self):
        graph = DiGraph()
        graph_algo = GraphAlgo(graph)
        graph.add_node(1, (32.25, 35.32, 0))
        self.assertEqual(graph.v_size(), 1)
        self.assertEqual(graph.e_size(), 0)
        self.assertEqual(graph_algo.get_graph().e_size(), 0)
        self.assertEqual(graph_algo.get_graph().v_size(), 1)
        self.assertEqual(graph_algo.shortest_path(1, 0), (None, []))
        self.assertEqual(graph_algo.shortest_path(0, 1), (None,[] ))

        self.assertEqual(graph_algo.connected_component(1), [1])
        self.assertEqual(graph_algo.connected_components(), [[1]])
        self.assertTrue(graph_algo.save_to_json('../data/one_node_graph'))
        self.assertTrue((graph_algo.load_from_json('../data/one_node_graph')))
        self.assertEqual(graph_algo.get_graph().get_all_v()[1].get_pos(), (32.25, 35.32, 0))
        self.assertEqual(graph_algo.get_graph().e_size(), 0)
        self.assertEqual(graph_algo.get_graph().v_size(), 1)

    def test_two_node_graph(self):
        graph = DiGraph()
        graph_algo = GraphAlgo(graph)
        self.assertTrue(graph.add_node(1))
        self.assertTrue(graph.add_node(2))
        self.assertEqual(graph.v_size(), 2)
        self.assertEqual(graph.e_size(), 0)
        self.assertEqual(graph_algo.shortest_path(1, 2), (math.inf, []))
        self.assertTrue(graph.add_edge(1, 2, 10))
        self.assertEqual(graph_algo.shortest_path(1, 2), (10, [1, 2]))
        self.assertEqual(graph_algo.connected_components(), [[2], [1]])
        self.assertEqual(graph_algo.connected_component(1), [1])
        self.assertEqual(graph_algo.connected_component(2), [2])
        self.assertTrue(graph.add_edge(2, 1, 8.33))
        self.assertEqual(graph_algo.shortest_path(2, 1), (8.33, [2, 1]))
        self.assertEqual(graph_algo.connected_components(), [[2, 1]])
        self.assertEqual(graph_algo.connected_component(1), [2, 1])
        self.assertEqual(graph_algo.connected_component(2), [1, 2])
        self.assertTrue(graph_algo.save_to_json('../data/two_node_graph'))

    def test_small_graph(self):

        g = DiGraph()
        algo = GraphAlgo(g)

        self.assertTrue(g.add_node(1))
        self.assertTrue(g.add_node(2))
        self.assertTrue(g.add_node(3))
        self.assertTrue(g.add_node(4))
        self.assertTrue(g.add_node(5))
        self.assertTrue(g.add_node(6))
        self.assertTrue(g.add_edge(1, 3, 9))
        self.assertTrue(g.add_edge(1, 2, 3.45))
        self.assertTrue(g.add_edge(1, 6, 14))
        self.assertTrue(g.add_edge(2, 3, 10))
        self.assertTrue(g.add_edge(2, 4, 2.34322))
        self.assertTrue(g.add_edge(3, 6, 2))
        self.assertTrue(g.add_edge(3, 4, 11))
        self.assertTrue(g.add_edge(4, 5, 6))
        self.assertTrue(g.add_edge(6, 5, 9))
        self.assertEqual(algo.connected_components(), [[5], [6], [4], [3], [2], [1]])
        self.assertTrue(g.add_edge(5, 3, 2.1211))
        self.assertTrue(g.add_edge(4, 2, 2.34322))
        self.assertTrue(g.add_edge(2, 1, 3.45))
        self.assertEqual(algo.connected_components(), [[2, 4, 5, 6, 3, 1]])
        self.assertEqual(algo.shortest_path(1, 5), (11.79322, [1, 2, 4, 5]))
        self.assertEqual(algo.shortest_path(4, 6), (10.1211, [4, 5, 3, 6]))
        self.assertTrue(g.add_node(7))
        self.assertEqual(algo.connected_components(), [[2, 4, 5, 6, 3, 1], [7]])
        self.assertEqual(algo.connected_component(7), [7])

        self.assertTrue(g.remove_node(7))
        self.assertEqual(algo.connected_components(), [[2, 4, 5, 6, 3, 1]])
        self.assertEqual(algo.connected_component(6), [1, 2, 4, 3, 5, 6])

    def test_big_graph(self):
        # graph with 8000000 edges and 1000000 nodes
        graph = DiGraph()
        graph_algo = GraphAlgo(graph)
        for i in range(1000000):
            graph.add_node(i)

        for i in range(1000000):
            if i < 1000000 and i % 2 == 0:
                graph.add_edge(i, i + 1, random.uniform(0, 1000))
            if i < 1000000 and i % 2 != 0:
                graph.add_edge(i, i + 1, random.uniform(0, 1000))
            graph.add_edge(1000000, i, random.uniform(0, 1000))
            graph.add_edge(i, 1000000, random.uniform(0, 1000))
            graph.add_edge(i, 100000, random.uniform(0, 1000))
            graph.add_edge(i, 10000, random.uniform(0, 1000))
            graph.add_edge(i, 1000, random.uniform(0, 1000))
            graph.add_edge(i, 100, random.uniform(0, 1000))
            graph.add_edge(i, 10, random.uniform(0, 1000))
            graph.add_edge(i, 200, random.uniform(0, 1000))
            graph.add_edge(250, i, random.uniform(0, 1000))
        self.assertEqual(len(graph_algo.connected_component(20)), 1000000)
        self.assertEqual(len(graph_algo.connected_components()[0]), 1000000)


if __name__ == '__main__':
    unittest.main()
