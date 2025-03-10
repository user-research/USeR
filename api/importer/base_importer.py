from config.config_parser import config
from helper.cleaner import Cleaner
import pandas as pd

class Importer:
    """
    Importer class
    """
    cleaner = Cleaner()

    def __init__(self, project: str):
        """
        Initialize the importer class

        Args:
            project (str): The project name
        """
        self.backlog_raw_file = config['project']['backlog_raw_file'].format(project=project)
        self.backlog_file = config['project']['backlog_file'].format(project=project)
        self.raw_backlog = pd.read_csv(
            self.backlog_raw_file, encoding='utf-8', keep_default_na=False)
        self.backlog = pd.DataFrame()

    def import_backlog(self):
        """
        Import the project backlog

        MANDATORY FIELDS:

        usid:                A unique technical number for the user story.
        text:                The user text combined, e.g., a title, description "As a persona,
                             I will ..., so ...", acceptance criteria, paths, and filenames.
        label_*:             These labels indicate whether the user story has the respective fields.
                             One means the field is present, and zero indicates it is not. This
                             information is used to train the Format Complete metric's support 
                             vector machine (SVM). Required fields (*):
                                - title
                                - persona
                                - what
                                - why
                                - acceptance_criteria
                                - attachments
                            The fields correspond to the configuration 'fields' in
                            ./api/config/default.cfg
        """
        raise NotImplementedError('Implement me in subclass')

    def get_backlog(self) -> pd.DataFrame:
        """
        Returns the backlog

        Returns:
            pd.DataFrame: The backlog
        """
        return self.backlog
