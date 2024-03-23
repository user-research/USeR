from config.user.UserConfigParser import config
from helper.Cleaner import Cleaner
import pandas as pd

class Importer(object):
    
    corpus = pd.DataFrame()
    raw_corpus = pd.DataFrame()
    cleaner = Cleaner()

    def __init__(self, project):
        self.corpus_raw_file = config['project']['corpus_raw_file'].format(project=project)
        self.corpus_file = config['project']['corpus_file'].format(project=project)
        self.raw_corpus = pd.read_csv(
            self.corpus_raw_file, encoding='utf-8', keep_default_na=False)

    def get_corpus(self):
        return self.corpus