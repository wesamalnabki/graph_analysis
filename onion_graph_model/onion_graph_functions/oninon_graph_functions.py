import pydot
import pandas as pd
import networkx as nx



class GraphFunctions(object):
    def __init__(self, processed_onion_dict):
        self.processed_onion_dict = processed_onion_dict

    def write_dataframe_xls(self, data_frame, file_name):
        # Create a Pandas Excel writer using XlsxWriter as the engine.
        writer = pd.ExcelWriter(file_name, engine='xlsxwriter')

        # Convert the dataframe to an XlsxWriter Excel object.
        data_frame.to_excel(writer, sheet_name='Sheet1')

        # Close the Pandas Excel writer and output the Excel file.
        writer.save()

    def calculate_degree(self, graph):
        print("Calculating degree...")
        g = graph
        deg = nx.degree(g)
        nx.set_node_attributes(g, 'degree', deg)
        return g, deg

    def calculate_indegree(self, graph):
        # will only work on DiGraph (directed graph)
        print("Calculating indegree...")
        g = graph
        indeg = g.in_degree()
        nx.set_node_attributes(g, 'indegree', indeg)
        return g, indeg

    def calculate_outdegree(self, graph):
        # will only work on DiGraph (directed graph)
        print("Calculating outdegree...")
        g = graph
        outdeg = g.out_degree()
        nx.set_node_attributes(g, 'outdegree', outdeg)
        return g, outdeg

    def calculate_betweenness(graph):
        print("Calculating betweenness...")
        g = graph
        bc = nx.betweenness_centrality(g)
        nx.set_node_attributes(g, 'betweenness', bc)
        return g, bc

    def calculate_eigenvector_centrality(self, graph):
        print("Calculating Eigenvector Centrality...")
        g = graph
        ec = nx.eigenvector_centrality(g)
        nx.set_node_attributes(g, 'eigen_cent', ec)
        # ec_sorted = sorted(ec.items(), key=itemgetter(1), reverse=True)
        # color=nx.get_node_attributes(G,'betweenness')  (returns a dict keyed by node ids)
        return g, ec

    def find_cliques(self, graph):
        # returns cliques as sorted list
        g = graph
        cl = nx.algorithms.find_cliques(g)
        cl = sorted(list(cl), key=len, reverse=True)
        print("Number of cliques:", len(cl))
        cl_sizes = [len(c) for c in cl]
        print("Size of cliques:", cl_sizes)
        return cl

    def graph_page_rank(self, graph, alpha=0.85):
        return nx.pagerank_scipy(graph, alpha=alpha)

    def is_node_in_graph(self, node_name, graph):
        if len(graph.get_node(name='"{0}"'.format(node_name))) > 0:
            return True
        return False

    def is_edge_in_graph(self, node_s, node_d, graph):
        if len(graph.get_edge(src_or_list=['"{0}"'.format(node_s), '"{0}"'.format(node_d)])) > 0:
            return True
        return False

    def create_class_graph(self, graph_total, data_frame, node_group, node_color, dir_list=[],
                           ignore_incoming_from_dict=True, ignore_outgoing_to_dict=True):
        # Create the graph:
        g = pydot.Cluster(graph_name=node_group)

        # Create Nodes
        for onion_df in data_frame.Onion:
            onion = self.processed_onion_dict[onion_df]

            if len(onion.get_onion()) > 30:
                continue

            node = pydot.Node(onion.get_onion(), style="filled", color=node_color)
            node.set_label(onion.get_main_class())
            node.set_group(node_group)

            g.add_node(node)

        # Create Edges
        for onion_df in data_frame.Onion:
            onion = self.processed_onion_dict[onion_df]

            # plot in-out going nodes:
            for out_node in onion.get_outgoing_links_onion():
                if ignore_outgoing_to_dict:
                    if out_node in dir_list:
                        continue

                # check if the out_node does not exist in the nodes list:
                if not self.is_node_in_graph(out_node, g):
                    # Create node & add it to the graph:
                    node = pydot.Node(out_node, style="filled", color="green")
                    node.set_group('Others_out')
                    node.set_label(out_node)
                    g.add_node(node)

                if not self.is_edge_in_graph(node_s=onion.get_onion(), node_d=out_node, graph=graph_total):
                    graph_total.add_edge(pydot.Edge(onion.get_onion(), out_node))

            for in_node in onion.get_incoming_links_onion():
                if ignore_incoming_from_dict:
                    if in_node in dir_list:
                        continue

                # check if the in_node does not exist in the nodes list:
                if not self.is_node_in_graph(in_node, g):
                    # Create node & add it to the graph:
                    node = pydot.Node(in_node, style="filled", color="blue")
                    node.set_group('Others_in')
                    node.set_label(in_node)
                    g.add_node(node)
                if not self.is_edge_in_graph(node_s=in_node, node_d=onion.get_onion(), graph=graph_total):
                    graph_total.add_edge(pydot.Edge(in_node, onion.get_onion()))

        return g, graph_total
