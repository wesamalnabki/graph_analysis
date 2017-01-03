import pydot
import json
import pandas as pd
import networkx as nx
from networkx.drawing import nx_pydot
from networkx.readwrite import json_graph

from operator import itemgetter
from itertools import chain, count


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
                       [(source, mapping[u]), (target, mapping[v]), ('arrows', 'to')]))
            for u, v, d in G.edges_iter(data=True)]

    return data

def save_to_jsonfile(filename, graph):
    _attrs = dict(id='id_onion', source='from', target='to', key='key')
    print('Dumping graph to JSON')

    g_json = node_link_data_mod(graph, _attrs)
    json.dump(g_json, open(filename, 'w'))
    json2js(filename)



def read_json_file(filename, info=True):
    graph = json_graph.load(open(filename))
    if info:
        print("Read in file ", filename)
        print(nx.info(graph))
    return graph



class GraphFunctions(object):
    def __init__(self, graph):
        self.graph = graph

    def find_cliques(self, ):
        # returns cliques as sorted list
        g = self.graph
        cl = nx.find_cliques(g)
        cl = sorted(list(cl), key=len, reverse=True)
        print("Number of cliques:", len(cl))
        cl_sizes = [len(c) for c in cl]
        print("Size of cliques:", cl_sizes)
        return cl

    def print_graph_info(self):
        print(nx.info(self.graph))

    def calculate_indegree(self):
        # will only work on DiGraph (directed graph)
        print("Calculating indegree...")
        g = self.graph
        indeg = g.in_degree()
        nx.set_node_attributes(g, 'indegree', indeg)
        return g, indeg

    def write_graph_dot_to_file(self, graph_directory):
        self.graph.write(graph_directory)

    @staticmethod
    def write_dataframe_xls(data_frame, file_name):
        # Create a Pandas Excel writer using XlsxWriter as the engine.
        writer = pd.ExcelWriter(file_name, engine='xlsxwriter')

        # Convert the dataframe to an XlsxWriter Excel object.
        data_frame.to_excel(writer, sheet_name='Sheet1')

        # Close the Pandas Excel writer and output the Excel file.
        writer.save()

    def calculate_degree(self):
        print("Calculating degree...")
        g = self.graph
        deg = nx.degree(g)
        nx.set_node_attributes(g, 'degree', deg)
        return g, deg

    def calculate_outdegree(self):
        # will only work on DiGraph (directed graph)
        print("Calculating outdegree...")
        g = self.graph
        outdeg = g.out_degree()
        nx.set_node_attributes(g, 'outdegree', outdeg)
        return g, outdeg

    def calculate_betweenness(self):
        print("Calculating betweenness...")
        g = self.graph
        bc = nx.betweenness_centrality(g)
        nx.set_node_attributes(g, 'betweenness', bc)
        return g, bc

    def calculate_eigenvector_centrality(self):
        print('Calculating Eigenvector Centrality...')
        g = self.graph
        try:
            ec = nx.eigenvector_centrality(g)
        except:
            print('Error, Could not find eigen_cent')
            ec = {}
            for onion in g.nodes():
                ec[onion] = 0
        nx.set_node_attributes(g, 'eigen_cent', ec)
        return g, ec

    def calculate_HITS_centrality(self):
        g = self.graph
        h, a = nx.hits_scipy(g, max_iter=900)
        nx.set_node_attributes(g, 'Hub', h)
        nx.set_node_attributes(g, 'authority', a)
        return g, h, a

    def find_density(self):
        return nx.density(self.graph)

    def find_cliques(self):
        ''' Calculate cliques and return as sorted list.  Print sizes of cliques found.
        '''
        graph = self.graph.to_undirected()
        g = graph
        cl = nx.find_cliques(g)
        cl = sorted(list(cl), key=len, reverse=True)
        # print ("Number of cliques:", len(cl))
        cl_sizes = [len(c) for c in cl]
        # print ("Size of cliques:", cl_sizes)
        return cl

    def find_cliques(self):
        # returns cliques as sorted list
        g = self.graph
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

    @staticmethod
    def set_node_attributes_onion(G, processed_onion_dict):
        # nx.set_edge_attributes(graph_all_nx, 'arrow')
        # for egde in G.edges():
        #    G.egde[egde]['arrow'] = 'to'
        mapping = dict(zip(G, count()))
        nx.set_node_attributes(G, 'id', mapping)
        for node in G.nodes():
            if node in processed_onion_dict.keys():
                obj = processed_onion_dict[node]
                G.node[node]['group'] = obj.get_main_class().split('/')[0]
                G.node[node]['label'] = obj.get_main_class()
                G.node[node]['onion'] = obj.get_onion()

                # else:
                #    G.node[node]['group'] = 'New_Node'
                #    G.node[node]['label'] = 'New_Node'
                #    G.node[node]['onion'] = node
                #    with open ('new.txt', 'a')as wr:
                #        wr.write (node+'\n')
        return G

    def calculate_degree_centrality(self):
        print("Calculating Degree Centrality...")
        g = self.graph
        dc = nx.degree_centrality(g)
        nx.set_node_attributes(g, 'degree_cent', dc)
        degcent_sorted = sorted(dc.items(), key=itemgetter(1), reverse=True)
        # for key, value in degcent_sorted[0:10]:
        #    print("Highest degree Centrality:", key, value)

        return g, dc

    def report_node_data(self, node=""):
        g = self.graph
        if len(node) == 0:
            print("Found these sample attributes on the nodes:")
            print(g.nodes(data=True)[0])
        else:
            print("Values for node " + node)
            print([d for n, d in g.nodes_iter(data=True) if n == node])

    def graph_page_rank(self, alpha=0.85):
        print('Calculating PageRank..')
        g = self.graph
        pr = nx.pagerank_scipy(g, alpha=alpha)
        nx.set_node_attributes(g, 'page_rank', pr)
        return g, pr

    def pydot_2_networkx(self):
        return nx.DiGraph(nx_pydot.from_pydot(self.graph))

    def networkx_2_pydot(self):
        return nx_pydot.to_pydot(self.graph)

    def return_node_followers(self, node):
        flw = []
        [flw.append(u) for (u, v) in self.graph.edges() if v == node]
        return flw

    def return_node_followings(self, node):
        return list(self.graph[node].keys())

    def calc(self, node_a, node_b):
        a = self.return_node_followers(node_a)
        b = self.return_node_followers(node_b)
        un_list = list(set(a).union(b))
        int_list = list(set(a).intersection(b))
        if len(un_list) == 0: return 0.0
        return 1 - (len(int_list) / len(un_list))

    def Katz_Rank(self):
        kc = nx.katz_centrality(self.graph, alpha=0.1, beta=1.0, max_iter=10000, tol=1e-06, nstart=None,
                                normalized=True,
                                weight='weight')
        nx.set_node_attributes(self.graph, 'katz_centrality', kc)
        return self.graph, kc

    def find_Rank_wesam(self):

        weight = {}
        rank = {}
        for node in self.graph:
            weight[node] = 0
            rank[node] = 0

        for node_case in self.graph:
            for node_follower in self.return_node_followers(node_case):
                # if node_follower == node_case:
                #    continue
                weight[node_follower] += self.calc(node_case, node_follower) * (
                    1 + len(self.return_node_followers(node_follower))) / len(self.graph.edges())

        for node_case in self.graph:
            for node_follower in self.return_node_followers(node_case):
                rank[node_case] += weight[node_follower]

        return rank
