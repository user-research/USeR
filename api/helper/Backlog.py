from config.user.UserConfigParser import config
import logging
import pandas as pd
import os

# https://docs.python.org/3/howto/logging.html
logging.basicConfig(
    filename=config['app']['sys_log_file'], format='%(levelname)s: %(asctime)s %(message)s', encoding='utf-8', level=logging.DEBUG)

class Backlog():
    '''
    Handles all access to the backlogs of user stories
    '''
    # Contains all project user stories
    backlogs = {}

    def __init__(self):
        self.load_all_backlogs()

    def get_backlog(self, project):
        """
        Returns project related user stories
        """
        return self.backlogs[project]
    
    def get_all(self):
        """
        Returns all project backlog and user stories
        """
        return self.backlogs
    
    def load_backlog(self, project):
        """
        Load user stories to a specific project
        """
        backlog = pd.DataFrame()
        backlog_file = config['project']['backlog_file'].format(project=project)

        if os.path.exists(backlog_file):
            backlog = pd.read_csv(backlog_file, encoding='utf-8')
        else:
            logging.error(f'backlog file {backlog_file} cannot be loaded')
        
        return backlog

    def load_all_backlogs(self):
        """
        Load all user stories from configured projects
        """
        projects = config['app']['projects'].split(r',')
        for project in projects:
            self.backlogs[project] = self.load_backlog(project)