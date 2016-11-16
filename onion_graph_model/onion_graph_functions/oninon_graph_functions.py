import pydot
import json
import pandas as pd
import networkx as nx
from networkx.drawing import nx_pydot
from networkx.readwrite import json_graph
from itertools import count, chain

import os
from operator import itemgetter
from itertools import count


def node_link_data_mod(G, attrs):
    multigraph = G.is_multigraph()
    id_ = attrs['id']
    source = attrs['source']
    target = attrs['target']
    # Allow 'key' to be omitted from attrs if the graph is not a multigraph.
    key = None if not multigraph else attrs['key']
    if len(set([source, target, key])) < 3:
        raise nx.NetworkXError('Attribute names are not unique.')
    mapping = dict(zip(G, count()))
    data = {}
    data['directed'] = G.is_directed()
    data['multigraph'] = multigraph
    data['graph'] = G.graph
    data['nodes'] = [dict(chain(G.node[n].items(), [(id_, n)])) for n in G]
    if multigraph:
        data['links'] = [
            dict(chain(d.items(),
                       [(source, mapping[u]), (target, mapping[v]), (key, k)]))
            for u, v, k, d in G.edges_iter(keys=True, data=True)]
    else:
        data['links'] = [
            dict(chain(d.items(),
                       [(source, u), (target, v)]))
            for u, v, d in G.edges_iter(data=True)]

    return data


def json2js(jsonfilepath, functionname='getData'):
    """function converting json file to javascript file: json_data -> json_data.js
    :param jsonfilepath: path to json file
    :param functionname: name of javascript function which will return the data
    :return None
    """
    # load json data
    with open(jsonfilepath, 'r') as jsonfile:
        data = json.load(jsonfile)
    # write transformed javascript file
    with open(jsonfilepath + '.js', 'w') as jsfile:
        jsfile.write('function ' + functionname + '(){return ')
        jsfile.write(json.dumps(data))
        jsfile.write(';}')

def save_to_jsonfile(filename, graph):
    _attrs = dict(id='id', source='from', target='to', key='key')
    print('Dumping graph to JSON')
    g = graph
    g_json = node_link_data_mod(g, _attrs)  # node-link format to serialize
    json.dump(g_json, open(filename, 'w'))


def read_json_file(filename, info=True):
    graph = json_graph.load(open(filename))
    if info:
        print("Read in file ", filename)
        print(nx.info(graph))
    return graph



class GraphFunctions(object):
    def __init__(self, processed_onion_dict):
        self.processed_onion_dict = processed_onion_dict

    def find_cliques(graph):
        # returns cliques as sorted list
        g = graph
        cl = nx.find_cliques(g)
        cl = sorted(list(cl), key=len, reverse=True)
        print("Number of cliques:", len(cl))
        cl_sizes = [len(c) for c in cl]
        print("Size of cliques:", cl_sizes)
        return cl

    @staticmethod
    def print_graph_info(graph):
        print(nx.info(graph))

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
        try:
            ec = nx.eigenvector_centrality(g)
        except:
            print('Error, Could not find eigen_cent')
            ec = {}
            for onion in g.nodes():
                ec[onion] = 0
        nx.set_node_attributes(g, 'eigen_cent', ec)
        return g, ec

    @staticmethod
    def calculate_HITS_centrality(graph):
        print('Calculating Hubs and authorities...')
        g = graph
        try:
            h, a = nx.hits_scipy(g)
        except:
            print('Error, Could not find Hubs and authorities')
            h, a = {}, {}
            for onion in g.nodes():
                a[onion] = 0
                h[onion] = 0
        nx.set_node_attributes(g, 'Hub', h)
        nx.set_node_attributes(g, 'authority', a)
        return g, h, a

    @staticmethod
    def find_density(graph):
        return nx.density(graph)

    @staticmethod
    def find_cliques(graph):
        ''' Calculate cliques and return as sorted list.  Print sizes of cliques found.
        '''
        graph = graph.to_undirected()
        g = graph
        cl = nx.find_cliques(g)
        cl = sorted(list(cl), key=len, reverse=True)
        # print ("Number of cliques:", len(cl))
        cl_sizes = [len(c) for c in cl]
        # print ("Size of cliques:", cl_sizes)
        return cl

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

    def dump_graph_xls(self, output_dir, graph):
        # Dump the results to xls file:
        df_pr = pd.DataFrame(columns=('Onion', 'group', 'degree',
                                      'indegree', 'outdegree', 'degree_cent',
                                      'eigen_cent', 'betweenness', 'page_rank'))

        for index, node in enumerate(graph.nodes()):
            n_d = graph.node[node]
            ## Check if node in ND
            try:
                df_pr.loc[index] = [n_d['onion'], n_d['group'], n_d['degree'],
                                    n_d['indegree'], n_d['outdegree'], n_d['degree_cent'],
                                    n_d['eigen_cent'], n_d['betweenness'], n_d['page_rank']]
            except:
                ## TODO add the not found node to DF
                df_pr.loc[index] = [n_d['onion'], 'New_Node', n_d['degree'],
                                    n_d['indegree'], n_d['outdegree'], n_d['degree_cent'],
                                    n_d['eigen_cent'], n_d['betweenness'], n_d['page_rank']]
                print(n_d)

        self.write_dataframe_xls(df_pr, output_dir + 'df_pr.xlsx')
        print('Finish dumping graph results')

    def set_node_attributes_onion(self, G):
        mapping = dict(zip(G, count()))
        nx.set_node_attributes(G, 'id', mapping)
        for node in G.nodes():
            if node in self.processed_onion_dict.keys():
                obj = self.processed_onion_dict[node]
                G.node[node]['group'] = obj.get_main_class()
                G.node[node]['label'] = obj.get_main_class()
                G.node[node]['onion'] = obj.get_onion()
            else:
                G.node[node]['group'] = 'New_Node'
                G.node[node]['label'] = 'New_Node'
                G.node[node]['onion'] = node
        return G

    def calculate_degree_centrality(self, graph):
        print("Calculating Degree Centrality...")
        g = graph
        dc = nx.degree_centrality(g)
        nx.set_node_attributes(g, 'degree_cent', dc)
        degcent_sorted = sorted(dc.items(), key=itemgetter(1), reverse=True)
        # for key, value in degcent_sorted[0:10]:
        #    print("Highest degree Centrality:", key, value)

        return graph, dc

    def report_node_data(self, graph, node=""):
        g = graph
        if len(node) == 0:
            print("Found these sample attributes on the nodes:")
            print(g.nodes(data=True)[0])
        else:
            print("Values for node " + node)
            print([d for n, d in g.nodes_iter(data=True) if n == node])

    def graph_page_rank(self, graph, alpha=0.85):
        print('Calculating PageRank..')
        g = graph
        pr = nx.pagerank_scipy(g, alpha=alpha)
        nx.set_node_attributes(g, 'page_rank', pr)
        return g, pr

    def is_node_in_graph(self, node_name, graph):
        if len(graph.get_node(name='"{0}"'.format(node_name))) > 0:
            return True
        return False

    def is_edge_in_graph(self, node_s, node_d, graph):
        if len(graph.get_edge(src_or_list=['"{0}"'.format(node_s), '"{0}"'.format(node_d)])) > 0:
            return True
        return False

    @staticmethod
    def pydot_2_networkx(graph):
        return nx.DiGraph(nx_pydot.from_pydot(graph))

    @staticmethod
    def networkx_2_pydot(graph):
        return nx_pydot.to_pydot(graph)


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

