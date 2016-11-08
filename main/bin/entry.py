import os
import re
import tldextract
from bs4 import BeautifulSoup
import graphviz as gv
import pydot
import pandas as pd

import networkx as nx
import pydotplus
from networkx.drawing import nx_pydot
from operator import itemgetter
from sklearn.externals import joblib

data_frame = pd.read_excel('/home/wesam/datasets/Manual_Classification_v16_FULL.xls', encoding='utf-8')


def save_classifer(clf, clf_name):
    joblib.dump(clf, clf_name + '.pkl', compress=9)
    print(clf_name + ' classifer has been saved!')


def load_classifer(clf_name):
    return joblib.load(clf_name + '.pkl')
