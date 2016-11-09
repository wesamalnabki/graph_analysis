import os

import tldextract
from bs4 import BeautifulSoup
import pydot
import pandas as pd

from networkx.drawing import nx_pydot
from sklearn.externals import joblib

from onion_graph_model.onion_graph_functions.oninon_graph_functions import GraphFunctions
from onion_graph_model.onion_node_model.onion_node_model import OnionGraphBuilder

dataset_dir = 'D:/Wesam/Onion_Dataset'
dataset_dir_xls = 'D:/Wesam/dataset xls/Manual_Classification_v16_FULL.xls'
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


def delete_links():
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


if __name__ == "__main__":
    data_frame = load_datafram()
    data_frame_social_network, data_frame_fraud, data_frame_cryptolocker, data_frame_politics, data_frame_leaked, \
    data_frame_Human_Trafficking, data_frame_Others, data_frame_religion, data_frame_unkown, data_frame_library, \
    data_frame_casino, data_frame_forum, data_frame_art, data_frame_services, data_frame_wiki, data_frame_marketplace, \
    data_frame_directory, data_frame_hosting, data_frame_drug, data_frame_cryptocurrency, data_frame_violence, \
    data_frame_porno, data_frame_hacking, data_frame_cc, data_frame_money, data_frame_locked, data_frame_pi = \
        load_subdatafram(data_frame)

    # delete_links(dataset_dir)
    # find_links_in_onion(dataset_dir, data_frame)

    if os.path.exists(output_dir + 'processed_onion_dict.pkl'):
        processed_onion_dict = load_obj('processed_onion_dict')
    else:
        processed_onion_dict = build_nodes_dic(data_frame)
        save_obj(processed_onion_dict, 'processed_onion_dict')

    # Create an object of GraphFunctions class
    graph_funs = GraphFunctions(processed_onion_dict)

    if not os.path.exists(output_dir + 'graph_all.dot'):
        dir_list = list(data_frame_directory.Onion) + list(data_frame_wiki.Onion)
        graph_all = pydot.Dot(graph_type='digraph')

        g1, graph_all = graph_funs.create_class_graph(graph_all, data_frame_drug, 'Drugs',
                                                      'red', dir_list)
        g2, graph_all = graph_funs.create_class_graph(graph_all, data_frame_porno, 'Porno',
                                                      'yellow', dir_list)
        # g3, graph_all = create_class_graph(graph_all, data_frame_cc, processed_onion_dict, 'CC', 'pink', dir_list)
        # g4, graph_all = create_class_graph(graph_all, data_frame_cryptocurrency, processed_onion_dict, 'Cryptocurrency',
        #  'gray', dir_list)
        # g5, graph_all = create_class_graph(graph_all, data_frame_hacking, processed_onion_dict, 'Hacking', 'black',
        #  dir_list)
        # g6, graph_all = create_class_graph(graph_all, data_frame_marketplace, processed_onion_dict, 'marketplace',
        #  '#3F8A36', dir_list)

        graph_all.add_subgraph(g1)
        graph_all.add_subgraph(g2)
        # graph_all.add_subgraph(g3)
        # graph_all.add_subgraph(g4)
        # graph_all.add_subgraph(g5)
        # graph_all.add_subgraph(g6)

        graph_all.write(output_dir + 'graph_all.dot')

    else:
        print('Graph already exist. Read from file')
        (graph_all,) = pydot.graph_from_dot_file(output_dir + 'graph_all.dot')

    # Convert Pydot graph to NetworkX format.
    g_nx = nx_pydot.from_pydot(graph_all)
    print('nodes:', len(g_nx.nodes()))
    print('edges:', len(g_nx.edges()))

    # Dump the results to xls file:
    df_pr = pd.DataFrame(columns=('Onion', 'Main_Class', 'In_Links', 'Out_Links', 'Weight'))

    # Calculate PR for the graph
    pr = graph_funs.graph_page_rank(g_nx)

    # Remove the file of new address
    if os.path.exists(output_dir + 'new_onion.txt'):
        os.remove(output_dir + 'new_onion.txt')

    for index, onion_address in enumerate(pr):
        if onion_address not in processed_onion_dict.keys():
            with open(output_dir + 'new_onion.txt', 'a') as writer:
                writer.writelines(onion_address + '\n')
        else:
            ob = processed_onion_dict[onion_address]
            if ob.get_onion() in g_nx.nodes():
                df_pr.loc[index] = [ob.get_onion(),
                                    ob.get_main_class(),
                                    g_nx.in_degree(ob.get_onion()),
                                    g_nx.out_degree(ob.get_onion()),
                                    pr[onion_address]
                                    ]
        graph_funs.write_dataframe_xls(df_pr, output_dir + 'df_pr.xlsx')
    print('Done!')
