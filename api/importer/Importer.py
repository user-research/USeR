from config.user.UserConfigParser import config
from helper.Cleaner import Cleaner
import pandas as pd

class Importer(object):
    
    backlog = pd.DataFrame()
    raw_backlog = pd.DataFrame()
    cleaner = Cleaner()

    def __init__(self, project):
        self.backlog_raw_file = config['project']['backlog_raw_file'].format(project=project)
        self.backlog_file = config['project']['backlog_file'].format(project=project)
        self.raw_backlog = pd.read_csv(
            self.backlog_raw_file, encoding='utf-8', keep_default_na=False)

    def get_backlog(self):
        return self.backlog