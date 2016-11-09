import pydot
import pandas as pd
import networkx as nx
from networkx.drawing import nx_pydot

import os
from operator import itemgetter






class GraphFunctions(object):
    def __init__(self, processed_onion_dict):
        self.processed_onion_dict = processed_onion_dict

    @staticmethod
    def print_graph_info(graph):
        print('nodes:', len(graph.nodes()))
        print('edges:', len(graph.edges()))

    @staticmethod
    def calculate_indegree(graph):
        # will only work on DiGraph (directed graph)
        print("Calculating indegree...")
        g = graph
        indeg = g.in_degree()
        nx.set_node_attributes(g, 'indegree', indeg)
        return g, indeg

    @staticmethod
    def write_graph_dot_to_file(graph, graph_directory):
        graph.write(graph_directory)

    @staticmethod
    def write_dataframe_xls(data_frame, file_name):
        # Create a Pandas Excel writer using XlsxWriter as the engine.
        writer = pd.ExcelWriter(file_name, engine='xlsxwriter')

        # Convert the dataframe to an XlsxWriter Excel object.
        data_frame.to_excel(writer, sheet_name='Sheet1')

        # Close the Pandas Excel writer and output the Excel file.
        writer.save()

    @staticmethod
    def calculate_degree(graph):
        print("Calculating degree...")
        g = graph
        deg = nx.degree(g)
        nx.set_node_attributes(g, 'degree', deg)
        return g, deg

    @staticmethod
    def calculate_outdegree(graph):
        # will only work on DiGraph (directed graph)
        print("Calculating outdegree...")
        g = graph
        outdeg = g.out_degree()
        nx.set_node_attributes(g, 'outdegree', outdeg)
        return g, outdeg

    @staticmethod
    def calculate_betweenness(graph):
        print("Calculating betweenness...")
        g = graph
        bc = nx.betweenness_centrality(g)
        nx.set_node_attributes(g, 'betweenness', bc)
        return g, bc

    @staticmethod
    def calculate_eigenvector_centrality(graph):
        print('Calculating Eigenvector Centrality...')
        g = graph
        ec = nx.eigenvector_centrality(g)
        nx.set_node_attributes(g, 'eigen_cent', ec)
        # ec_sorted = sorted(ec.items(), key=itemgetter(1), reverse=True)
        # color=nx.get_node_attributes(G,'betweenness')  (returns a dict keyed by node ids)
        return g, ec

    @staticmethod
    def find_cliques(graph):
        # returns cliques as sorted list
        g = graph
        cl = nx.algorithms.find_cliques(g)
        cl = sorted(list(cl), key=len, reverse=True)
        print("Number of cliques:", len(cl))
        cl_sizes = [len(c) for c in cl]
        print("Size of cliques:", cl_sizes)
        return cl

    def dump_pagr_rank_results(self, output_dir, pr, graph):
        # Dump the results to xls file:
        df_pr = pd.DataFrame(columns=('Onion', 'Main_Class', 'In_Links', 'Out_Links', 'Weight'))

        # Remove the file of new address
        if os.path.exists(output_dir + 'new_onion.txt'):
            os.remove(output_dir + 'new_onion.txt')

        for index, onion_address in enumerate(pr):
            if onion_address not in self.processed_onion_dict.keys():
                with open(output_dir + 'new_onion.txt', 'a') as writer:
                    writer.writelines(onion_address + '\n')
            else:
                ob = self.processed_onion_dict[onion_address]
                if ob.get_onion() in graph.nodes():
                    df_pr.loc[index] = [ob.get_onion(),
                                        ob.get_main_class(),
                                        graph.in_degree(ob.get_onion()),
                                        graph.out_degree(ob.get_onion()),
                                        pr[onion_address]
                                        ]
        self.write_dataframe_xls(df_pr, output_dir + 'df_pr.xlsx')
        print('Finish dumping pageRank results')

    def calculate_degree_centrality(self, graph):
        print("Calculating Degree Centrality...")
        g = graph
        dc = nx.degree_centrality(g)
        nx.set_node_attributes(g, 'degree_cent', dc)
        degcent_sorted = sorted(dc.items(), key=itemgetter(1), reverse=True)
        for key, value in degcent_sorted[0:10]:
            print("Highest degree Centrality:", key, value)

        return graph, dc

    def report_node_data(graph, node=""):
        g = graph
        if len(node) == 0:
            print("Found these sample attributes on the nodes:")
            print(g.nodes(data=True)[0])
        else:
            print("Values for node " + node)
            print([d for n, d in g.nodes_iter(data=True) if n == node])

    def graph_page_rank(self, graph, alpha=0.85):
        print('Calculating PageRank..')
        return nx.pagerank_scipy(graph, alpha=alpha)

    def is_node_in_graph(self, node_name, graph):
        if len(graph.get_node(name='"{0}"'.format(node_name))) > 0:
            return True
        return False

    def is_edge_in_graph(self, node_s, node_d, graph):
        if len(graph.get_edge(src_or_list=['"{0}"'.format(node_s), '"{0}"'.format(node_d)])) > 0:
            return True
        return False

    @staticmethod
    def convert_multidirectedgraph_to_simpledirectedgraph(graph):
        # Convert Pydot graph to NetworkX format.
        graph_nx = nx_pydot.from_pydot(graph)

        # Covert the MultiDirectedGraph to Simple Directed Graph:
        G = nx.DiGraph()
        for u, v in graph_nx.edges_iter(data=False):
            G.add_edge(u, v)
        return G

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

