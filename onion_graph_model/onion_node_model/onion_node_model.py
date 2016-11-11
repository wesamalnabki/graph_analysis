import os


class OnionGraphBuilder(object):
    def __init__(self, dataset_dir, onion_sample):

        self.dataset_dir = dataset_dir


        self.incoming_links_onion = []
        self.incoming_links_all = []
        self.incoming_links_surface = []
        self.outgoing_links_onion = []
        self.outgoing_links_all = []
        self.outgoing_links_surface = []

        self.lang = onion_sample.Lang
        self.text = onion_sample.Text
        self.text_hash = onion_sample.Hash
        self.onion = onion_sample.Onion
        self.main_class = onion_sample.Main_Class
        self.ID = onion_sample.ID

    def find_outgoing_links(self):
        onion_file = self.dataset_dir + '/{0}/{0}.lnk'.format(self.onion)
        if os.path.isfile(onion_file):
            with open(onion_file, 'r', encoding='utf-8') as red:
                extracted_links = red.readlines()
                for link in extracted_links:
                    link = link.strip().replace('\xad', '')
                    if link.endswith('.onion'):
                        self.outgoing_links_onion.append(link)
                    else:
                        self.outgoing_links_surface.append(link)
                    self.outgoing_links_all.append(link)

    def find_incoming_links(self):
        all_onion_links = os.listdir(self.dataset_dir)
        for link in all_onion_links:
            if link == self.onion:
                continue
            onion_file = self.dataset_dir + '/{0}/{0}.lnk'.format(link)
            if os.path.isfile(onion_file):
                with open(onion_file, 'r', encoding='utf-8') as red:
                    extracted_links = red.readlines()
                    extracted_links = [onion_link.strip().replace('\xad', '') for onion_link in extracted_links]
                    if self.onion in extracted_links:
                        if link.endswith('.onion'):
                            self.incoming_links_onion.append(link)
                        else:
                            self.incoming_links_surface.append(link)
                        self.incoming_links_all.append(link)

    def append_to_incomming_list_all(self, incoming_onion):
        self.incoming_links_all.append(incoming_onion)

    def append_to_incomming_list_onion(self, incoming_onion):
        self.incoming_links_onion.append(incoming_onion)

    def append_to_incomming_list_surface(self, incoming_onion):
        self.incoming_links_surface.append(incoming_onion)

    def get_outgoing_links_all(self):
        return list(set(self.outgoing_links_all))

    def get_outgoing_links_onion(self):
        return list(set(self.outgoing_links_onion))

    def get_outgoing_links_surface(self):
        return list(set(self.outgoing_links_surface))

    def get_incoming_links_all(self):
        return list(set(self.incoming_links_all))

    def get_incoming_links_onion(self):
        return list(set(self.incoming_links_onion))

    def get_incoming_links_surface(self):
        return list(set(self.incoming_links_surface))

    def get_incoming_count(self):
        return len(list(set(self.incoming_links_all)))

    def get_outgoing_count(self):
        return len(list(set(self.outgoing_links_all)))

    def get_onion(self):
        return self.onion

    def get_main_class(self):
        return self.main_class

    def get_onion_text(self):
        return self.text

    def get_onion_hash(self):
        return self.text_hash

    def get_onion_lang(self):
        return self.lang

    def get_onion_ID(self):
        return self.ID
