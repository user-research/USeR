from config.user.UserConfigParser import config
import logging
import pandas as pd
import os

# https://docs.python.org/3/howto/logging.html
logging.basicConfig(
    filename=config['app']['sys_log_file'], format='%(levelname)s: %(asctime)s %(message)s', encoding='utf-8', level=logging.DEBUG)

class Corpora():
    '''
    Handles all access to corpora/backlog of user stories
    '''
    # Contains all project user stories
    corpora = {}

    def __init__(self):
        self.load_corpora()

    def get_corpus(self, project):
        """
        Returns project related user stories
        """
        return self.corpora[project]
    
    def get_all(self):
        """
        Returns all project corpora and user stories
        """
        return self.corpora
    
    def load_corpus(self, project):
        """
        Load user stories to a specific project
        """
        corpus = pd.DataFrame()
        corpus_file = config['project']['corpus_file'].format(project=project)

        if os.path.exists(corpus_file):
            corpus = pd.read_csv(corpus_file, encoding='utf-8')
        else:
            logging.error(f'Corpus file {corpus_file} cannot be loaded')
        
        return corpus

    def load_corpora(self):
        """
        Load all user stories from configured projects
        """
        projects = config['app']['projects'].split(r',')
        for project in projects:
            self.corpora[project] = self.load_corpus(project)