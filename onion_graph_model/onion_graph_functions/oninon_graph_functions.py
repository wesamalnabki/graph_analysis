import pydot
import pandas as pd


class GraphFunctions(object):
    def __init__(self, processed_onion_dict):
        self.processed_onion_dict = processed_onion_dict

    def write_dataframe_xls(data_frame, file_name):
        # Create a Pandas Excel writer using XlsxWriter as the engine.
        writer = pd.ExcelWriter(file_name, engine='xlsxwriter')

        # Convert the dataframe to an XlsxWriter Excel object.
        data_frame.to_excel(writer, sheet_name='Sheet1')

        # Close the Pandas Excel writer and output the Excel file.
        writer.save()

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
        # g = pydot.Dot(graph_type='digraph')
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
                # if out_node in dir_list:
                #    continue

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
                # if in_node in dir_list:
                #    continue

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
