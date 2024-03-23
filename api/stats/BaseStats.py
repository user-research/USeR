from config.user.UserConfigParser import config
import logging
import numpy as np
import os
import pandas as pd

# https://stackoverflow.com/questions/25351968/how-to-display-full-non-truncated-dataframe-information-in-html-when-convertin
pd.set_option('display.max_colwidth', None)

# https://docs.python.org/3/howto/logging.html
logging.basicConfig(
    filename=config['app']['sys_log_file'], format='%(levelname)s: %(asctime)s %(message)s', encoding='utf-8', level=logging.DEBUG)

class BaseStats(object):
    """
    BaseStats class
    """
    def __init__(self, setting='', project=''):
        self.correlations = []
        self.mlm_stats_file = ''
        self.percentiles = []
        self.plspm_calc = None
        self.project = project
        self.predictions = pd.DataFrame()
        self.setting = setting
    
    def get_predictions(self):
        """
        Retrieve the predictions based on computation and expert ratings
        """
        if self.predictions.empty:
            self.generate_predictions()

        return self.predictions

    def generate_predictions(self):
        raise NotImplementedError('Implement me in subclass')
    
    def generate_percentiles(self):
        """
        Generate percentiles based on predictions
        """
        # Set cache file on project level
        if self.setting == 'global':
            percentiles_file = config[self.setting]['percentiles_file']
        else:
            # Set cache file on project level
            percentiles_file = config[self.setting]['percentiles_file'].format(project=self.project)

        if os.path.exists(percentiles_file):
            self.percentiles = pd.read_csv(percentiles_file, encoding='utf-8').to_dict("records")
        else:
            predictions = self.get_predictions()

            percentiles = []
            metrics = config['app']['metrics'].split(r',')

            for indicator in metrics:
                tmp_predictions = predictions.loc[:, indicator]

                _20_percentile = np.percentile(tmp_predictions, 20)
                _33_percentile = np.percentile(tmp_predictions, 33)
                _40_percentile = np.percentile(tmp_predictions, 40)
                _60_percentile = np.percentile(tmp_predictions, 60)
                _66_percentile = np.percentile(tmp_predictions, 66)
                _80_percentile = np.percentile(tmp_predictions, 80)
                _99_percentile = np.percentile(tmp_predictions, 99)

                percentiles.append({
                        'indicator':indicator, 
                        '_20':_20_percentile,
                        '_33':_33_percentile,
                        '_40':_40_percentile, 
                        '_60':_60_percentile,
                        '_66':_66_percentile,
                        '_80':_80_percentile,
                        '_99':_99_percentile,
                    })

            self.percentiles = percentiles
            pd.DataFrame(self.percentiles).to_csv(percentiles_file, index=False)

    def get_percentiles(self, name=''):
        """
        Retrieve the percentiles based on computation and expert ratings
        """
        if self.percentiles == []:
            self.generate_percentiles()
        if name != '': 
            for tmp_percentiles in self.percentiles:
                if tmp_percentiles['indicator'] == name:
                    return tmp_percentiles
                
        return self.percentiles