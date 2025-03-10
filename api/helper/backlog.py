from config.config_parser import config
import logging
import os
import pandas as pd

# https://docs.python.org/3/howto/logging.html
logging.basicConfig(
    filename=config['app']['sys_log_file'],
    format='%(levelname)s: %(asctime)s %(message)s',
    encoding='utf-8', level=logging.DEBUG)

class Backlog:
    """
    Handles all access to the backlogs of user stories
    """
    # Contains all project user stories
    backlogs = {}

    def __init__(self):
        """
        Initialize the backlog class
        """
        self.load_all_backlogs()

    def get_backlog(self, project: str) -> pd.DataFrame:
        """
        Returns project related user stories

        Args:
            project (str): The project name
        """
        return self.backlogs[project]

    def get_all(self) -> dict:
        """
        Returns all project backlog and user stories

        Returns:
            dict: The project backlogs
        """
        return self.backlogs

    def load_backlog(self, project: str) -> pd.DataFrame:
        """
        Load user stories to a specific project

        Args:
            project (str): The project
        """
        backlog = pd.DataFrame()
        backlog_file = config['project']['backlog_file'].format(project=project)

        if os.path.exists(backlog_file):
            backlog = pd.read_csv(backlog_file, encoding='utf-8')
        else:
            logging.error('Backlog file %s cannot be loaded', backlog_file)

        return backlog

    def load_all_backlogs(self):
        """
        Load all user stories from configured projects
        """
        projects = config['app']['projects'].split(r',')
        for project in projects:
            self.backlogs[project] = self.load_backlog(project)
