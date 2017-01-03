import tldextract
from bs4 import BeautifulSoup

from sklearn.externals import joblib
import os
from onion_graph_model.onion_graph_functions.oninon_graph_functions import *  # save_to_jsonfile, read_json_file
from onion_graph_model.onion_node_model.onion_node_model import OnionGraphBuilder
from networkx.readwrite import json_graph
from operator import itemgetter

import networkx as nx


dataset_dir = 'D:/Wesam/Onion_Dataset'
dataset_dir_xls = 'D:/Wesam/dataset xls/DF_17.xlsx'
output_dir = 'D:/Wesam/Graph_Analysis_Results/'


def save_obj(clf, obj_name):
    joblib.dump(clf, output_dir + obj_name + '.pkl', compress=9)
    print(obj_name + ' Object has been saved!')


def load_obj(obj_name):
    obj = joblib.load(output_dir + obj_name + '.pkl')
    print(obj_name + ' Object has been loaded!')
    return obj


def load_datafram(dataframe_dir=dataset_dir_xls):
    return pd.read_excel(dataframe_dir, encoding='utf-8')


def load_subdatafram(data_frame):
    data_frame_social_network = pd.concat([data_frame[data_frame.Main_Class == 'Social-Network/ Email'],
                                           data_frame[data_frame.Main_Class == 'Social-Network/ Blog'],
                                           data_frame[data_frame.Main_Class == 'Social-Network/ Chat'],
                                           data_frame[data_frame.Main_Class == 'Social-Network/ News']],
                                          ignore_index=True)

    data_frame_fraud = data_frame[data_frame.Main_Class == 'Fraud']

    data_frame_cryptolocker = data_frame[data_frame.Main_Class == 'cryptolocker']

    data_frame_politics = data_frame[data_frame.Main_Class == 'Politics']

    data_frame_leaked = data_frame[data_frame.Main_Class == 'Leaked-Data']

    data_frame_Human_Trafficking = data_frame[data_frame.Main_Class == 'Human-Trafficking']

    data_frame_Others = data_frame[data_frame.Main_Class == 'Others']

    data_frame_religion = data_frame[data_frame.Main_Class == 'Religion']

    data_frame_unkown = data_frame[data_frame.Main_Class == 'Unkown']

    data_frame_library = data_frame[data_frame.Main_Class == 'Library/ Books']

    data_frame_casino = data_frame[data_frame.Main_Class == 'Casino/ Gambling']

    data_frame_forum = data_frame[data_frame.Main_Class == 'Forum']

    data_frame_art = data_frame[data_frame.Main_Class == 'Art/ Music']

    data_frame_services = data_frame[data_frame.Main_Class == 'Services']

    data_frame_wiki = data_frame[data_frame.Main_Class == 'Wiki']

    data_frame_marketplace = pd.concat([data_frame[data_frame.Main_Class == 'Marketplace/ Black'],
                                        data_frame[data_frame.Main_Class == 'Marketplace/ White']],
                                       ignore_index=True)

    data_frame_directory = data_frame[data_frame.Main_Class == 'Hosting/ Directory']
    data_frame_hosting = pd.concat([data_frame[data_frame.Main_Class == 'Hosting/ Server'],
                                    data_frame[data_frame.Main_Class == 'Hosting/ File-Sharing'],
                                    # data_frame[data_frame.Main_Class=='Hosting/ Directory'],
                                    data_frame[data_frame.Main_Class == 'Hosting/ Software'],
                                    data_frame[data_frame.Main_Class == 'Hosting/ Search-Engine'],
                                    data_frame[data_frame.Main_Class == 'Hosting/ Folders']],
                                   ignore_index=True)

    data_frame_drug = pd.concat([data_frame[data_frame.Main_Class == 'Drugs/ Ilegal'],
                                 data_frame[data_frame.Main_Class == 'Drugs/ Legal']],
                                ignore_index=True)

    data_frame_cryptocurrency = data_frame[data_frame.Main_Class == 'Cryptocurrency']

    data_frame_violence = pd.concat([data_frame[data_frame.Main_Class == 'Violence/ Hitman'],
                                     data_frame[data_frame.Main_Class == 'Violence/ Weapons'],
                                     data_frame[data_frame.Main_Class == 'Violence/ Hate']],
                                    ignore_index=True)

    data_frame_porno = pd.concat([data_frame[data_frame.Main_Class == 'Porno/ General-pornography'],
                                  data_frame[data_frame.Main_Class == 'Porno/ Child-pornography']],
                                 ignore_index=True)

    data_frame_hacking = data_frame[data_frame.Main_Class == 'Hacking']

    data_frame_cc = data_frame[data_frame.Main_Class == 'Counterfeit Credit-Cards']

    data_frame_money = data_frame[data_frame.Main_Class == 'Counterfeit Money']

    data_frame_locked = data_frame[data_frame.Main_Class == 'Locked']

    data_frame_pi = pd.concat(
        [data_frame[data_frame.Main_Class == 'Counterfeit Personal-Identification/  Driving-Licence'],
         data_frame[data_frame.Main_Class == 'Counterfeit Personal-Identification/ ID'],
         data_frame[data_frame.Main_Class == 'Counterfeit Personal-Identification/ Passport']],
        ignore_index=True)

    return data_frame_social_network, data_frame_fraud, data_frame_cryptolocker, data_frame_politics, data_frame_leaked, \
           data_frame_Human_Trafficking, data_frame_Others, data_frame_religion, data_frame_unkown, data_frame_library, \
           data_frame_casino, data_frame_forum, data_frame_art, data_frame_services, data_frame_wiki, data_frame_marketplace, \
           data_frame_directory, data_frame_hosting, data_frame_drug, data_frame_cryptocurrency, data_frame_violence, data_frame_porno, \
           data_frame_hacking, data_frame_cc, data_frame_money, data_frame_locked, data_frame_pi


def delete_links(data_frame):
    for onion in data_frame.Onion:
        onion_file = dataset_dir + '/{0}/{0}.lnk'.format(onion)
        if (os.path.exists(onion_file)):
            os.remove(onion_file)


def return_links(refs):
    extracted_links = []
    for ref in refs:
        link = tldextract.extract(ref)
        if len(link.domain) > 0 and len(link.suffix) > 0:
            link = '{0}.{1}'.format(link.domain, link.suffix)
            extracted_links.append(link)
    return list(set(extracted_links))


def return_all_links(onion):
    extracted_links1, extracted_links2 = [], []
    onion_file = dataset_dir + '/{0}/{0}.txt'.format(onion)
    with open(onion_file, 'rb') as red:
        text = red.readlines()
        if b'References\n' in text:
            idx = text.index(b'References\n')
            refs = text[idx:]
            refs = [('.'.join((ref.strip().decode('latin-1')).split('.')[1:])).strip() for ref in refs if
                    len(ref) > 10]
            extracted_links1 = return_links(refs)

    onion_file = dataset_dir + '/{0}/{0}.html'.format(onion)
    with open(onion_file, 'r', encoding='latin-1') as red:
        text = red.readlines()
        text = ' '.join([line.strip() for line in text])
        refs = []
        soup = BeautifulSoup(text, 'lxml')
        for link in soup.find_all('a', href=True):
            refs.append(link['href'])
        extracted_links2 = return_links(refs)
    return list(set(extracted_links1 + extracted_links2))


def find_links_in_onion(data_frame):
    for onion in data_frame.Onion:
        extracted_links = return_all_links(onion)
        if len(extracted_links) > 0:
            with open(dataset_dir + '/{0}/{0}.lnk'.format(onion), 'w', encoding='utf-8') as wrtr:
                [wrtr.write(extracted_link + '\n') for extracted_link in extracted_links]


def build_nodes_dic(data_frame):
    processed_onion_dict = {}
    print('building nodes dictionary...')
    for index, onion_sample in data_frame.iterrows():
        onion_graph_builder = OnionGraphBuilder(dataset_dir, onion_sample)
        onion_graph_builder.find_outgoing_links()
        processed_onion_dict[onion_sample.Onion] = onion_graph_builder

    for index, onion_sample in processed_onion_dict.items():
        link = onion_sample.get_onion()
        in_all = onion_sample.get_outgoing_links_all()
        for in_single in in_all:
            if in_single in processed_onion_dict.keys():  # and in_single !=link:
                if link.endswith('.onion'):
                    processed_onion_dict[in_single].append_to_incomming_list_onion(link)
                else:
                    processed_onion_dict[in_single].append_to_incomming_list_surface(link)
                processed_onion_dict[in_single].append_to_incomming_list_all(link)
    print('Finished building nodes dictionary...')
    return processed_onion_dict


def build_graphs(G, processed_onion_dict, dir_list, class_name, consider_dic=False):
    for onion in processed_onion_dict.values():
        if len(onion.get_onion()) > 30:
            continue
        if onion.get_main_class().startswith(class_name):
            G.add_node(onion.get_onion())
            for in_link in onion.get_incoming_links_onion():
                if not consider_dic:
                    if in_link in dir_list:
                        continue
                G.add_edge(in_link, onion.get_onion())

            for out_link in onion.get_outgoing_links_onion():
                if not consider_dic:
                    if out_link in dir_list:
                        continue
                G.add_edge(onion.get_onion(), out_link)

    return GraphFunctions.set_node_attributes_onion(G, processed_onion_dict)

# python -m http.server -b 127.0.0.1

def main():
    # delete_links(data_frame)
    # find_links_in_onion(data_frame)
    data_frame = load_datafram()

    dir_list_1 = data_frame[data_frame.Main_Class == 'Hosting/ Directory'].Onion
    dir_list_2 = data_frame[data_frame.Main_Class == 'Wiki'].Onion
    dir_list = list(dir_list_1) + list(dir_list_2)
    # dir_list = []

    if os.path.exists(output_dir + 'processed_onion_dict.pkl'):
        processed_onion_dict = load_obj('processed_onion_dict')
    else:
        processed_onion_dict = build_nodes_dic(data_frame)
        save_obj(processed_onion_dict, 'processed_onion_dict')

    graphs_list = []
    classes = ['Cryptocurrency', 'Drugs', 'Porno', 'Marketplace', 'Counterfeit Credit-Cards',
               'Library', 'Violence', 'Counterfeit Personal-Identification', 'Counterfeit Money',
               'Social-Network', 'Locked', 'Unkown', 'Down', 'Forum', 'Hacking', 'Casino',
               'Art', 'Religion', 'cryptolocker', 'Others']

    for class_name in classes:

        print('procrssing class:' + class_name)
        G = nx.DiGraph()
        G = build_graphs(G, processed_onion_dict, dir_list, class_name, False)

        if class_name == '':
            save_obj(G, 'ALL_f')
            save_to_jsonfile(output_dir + 'ALL_f' + '/' + 'ALL_f' + '.json', G)

        graph_funs = GraphFunctions(G)

        if class_name != '':
            print('Find Katz RANK')
            G, kr = graph_funs.Katz_Rank()
            kr_s = sorted(kr.items(), key=itemgetter(1), reverse=True)
            kr_s_dic = {}
            for idx, elm in enumerate(kr_s):
                kr_s_dic[elm[0]] = idx
            nx.set_node_attributes(G, 'katz_Rank', kr_s_dic)

        print('Find Wesam RANK')
        my_rank = graph_funs.find_Rank_wesam()
        my_rank_s = sorted(my_rank.items(), key=itemgetter(1), reverse=True)
        pr_dic = {}
        for idx, elm in enumerate(my_rank_s):
            pr_dic[elm[0]] = idx
        nx.set_node_attributes(G, 'W_Rank', pr_dic)

        print('Find HIST RANK')
        G, hub, auth = graph_funs.calculate_HITS_centrality()
        HITS_auth_rank = sorted(auth.items(), key=itemgetter(1), reverse=True)
        rank_dic = {}
        for idx, elm in enumerate(HITS_auth_rank):
            rank_dic[elm[0]] = idx
        nx.set_node_attributes(G, 'HITS_Auth_Rank', rank_dic)

        HITS_hub_rank = sorted(hub.items(), key=itemgetter(1), reverse=True)
        rank_dic = {}
        for idx, elm in enumerate(HITS_hub_rank):
            rank_dic[elm[0]] = idx
        nx.set_node_attributes(G, 'HITS_Hub_rank', rank_dic)

        print('Find EV RANK')
        G, eigen = graph_funs.calculate_eigenvector_centrality()
        ev_s = sorted(eigen.items(), key=itemgetter(1), reverse=True)
        ev_dic = {}
        for idx, elm in enumerate(ev_s):
            ev_dic[elm[0]] = idx
        nx.set_node_attributes(G, 'EV_Rank', ev_dic)

        # Graph Analysis
        print('Find PR RANK')
        G, pr = graph_funs.graph_page_rank()
        pr_s = sorted(pr.items(), key=itemgetter(1), reverse=True)
        pr_dic = {}
        for idx, elm in enumerate(pr_s):
            pr_dic[elm[0]] = idx
        nx.set_node_attributes(G, 'PR_Rank', pr_dic)

        G, deg = graph_funs.calculate_degree()
        G, indeg = graph_funs.calculate_indegree()
        G, outdeg = graph_funs.calculate_outdegree()
        # G, betwndeg = graph_funs.calculate_betweenness()

        G, degcent = graph_funs.calculate_degree_centrality()

        # clique = graph_funs.find_cliques(G)
        # density = graph_funs.find_density(G)


        graph_funs.print_graph_info()

        if class_name == '':
            class_name = 'ALL'

        if not os.path.exists(output_dir + class_name + '/'):
            os.makedirs(output_dir + class_name + '/')

        graphs_list.append(G)
        save_to_jsonfile(output_dir + class_name + '/' + class_name + '.json', G)
        save_obj(graphs_list, 'graphs_list')
        json_graph


if __name__ == "__main__":
    H = nx.read_gml('lesmis.gml')

    graph_funs = GraphFunctions(H)

    print('Find Wesam RANK')
    my_rank = graph_funs.find_Rank_wesam()
    my_rank_s = sorted(my_rank.items(), key=itemgetter(1), reverse=True)
    pr_dic = {}
    for idx, elm in enumerate(my_rank_s):
        pr_dic[elm[0]] = idx
    nx.set_node_attributes(H, 'W_Rank', pr_dic)

    save_to_jsonfile(output_dir + 'lesmis' + '/' + 'lesmis' + '.json', H)

    main()
