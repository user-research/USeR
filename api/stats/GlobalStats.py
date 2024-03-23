import pandas as pd
import os
from config.user.UserConfigParser import config
from stats.BaseStats import BaseStats
from stats.ProjectStats import ProjectStats

# https://stackoverflow.com/questions/25351968/how-to-display-full-non-truncated-dataframe-information-in-html-when-convertin
pd.set_option('display.max_colwidth', None)

class GlobalStats(BaseStats):
    """
    GlobalStats class
    """
    def __init__(self, setting='global'):
        super().__init__(setting=setting)

        # Setup mlm stats cache file
        self.mlm_stats_file = config[self.setting]['mlm_stats_file']

    def generate_predictions(self):
        """
        Setup experts ratings file for computational ratings' evaluations
        """
        predictions_file = config[self.setting]['predictions_file']

        if os.path.exists(predictions_file):
            self.predictions = pd.read_csv(predictions_file, encoding='utf-8')
        else:
            pm1 = ProjectStats(project = 'p1')
            pm2 = ProjectStats(project = 'p2')

            predictions_p1 = pm1.get_predictions()
            predictions_p2 = pm2.get_predictions()

            self.predictions = pd.concat([predictions_p1, predictions_p2], ignore_index=True) \
                                 .sort_values(by=['comp_total'])
            self.predictions.to_csv(
                predictions_file, index=False)
        
        return self.predictions