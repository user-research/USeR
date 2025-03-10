from config.config_parser import config
import os
import pandas as pd
from stats.base_stats import BaseStats
from stats.project_stats import ProjectStats

# https://stackoverflow.com/questions/25351968/how-to-display-full-non-truncated-dataframe-information-in-html-when-convertin
pd.set_option('display.max_colwidth', None)

class GlobalStats(BaseStats):
    """
    GlobalStats class
    """
    def __init__(self, setting='global'):
        """
        Initialize the global stats class

        Args:
            setting (str): The setting
        """
        super().__init__(setting=setting)
        self.predictions = pd.DataFrame()

    def generate_predictions(self) -> pd.DataFrame:
        """
        Setup experts ratings file for computational ratings' evaluations
        """
        predictions_file = config[self.setting]['predictions_file']

        if os.path.exists(predictions_file):
            self.predictions = pd.read_csv(predictions_file, encoding='utf-8')
        else:
            print("Generating global predictions ...")
            predictions = []
            for project in config['app']['projects'].split(r','):
                stats = ProjectStats(project)
                predictions.append(stats.get_predictions())
            self.predictions = pd.concat(
                predictions, ignore_index=True).sort_values(by=['comp_total'])
            self.predictions.to_csv(predictions_file, index=False)

        return self.predictions
