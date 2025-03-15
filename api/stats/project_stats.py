from config.config_parser import config
from metrics.metrics import Metrics
import os
import pandas as pd
from stats.base_stats import BaseStats
from tqdm import tqdm

# https://stackoverflow.com/questions/25351968/how-to-display-full-non-truncated-dataframe-information-in-html-when-convertin
pd.set_option('display.max_colwidth', None)

class ProjectStats(BaseStats):
    """
    ProjectStats class
    """
    def __init__(self, project="p1"):
        """
        Initialize the project stats class

        Args:
            project (str): The project name
        """
        super().__init__(setting='project', project=project)
        self.predictions = pd.DataFrame()

        # Add the full backlog to query user stories
        self.backlog = pd.read_csv(
            config[self.setting]['backlog_file'].format(project=self.project), encoding='utf-8')

    def generate_predictions(self):
        """
        Generate predictions for a project
        """
        predictions_file = config[self.setting]['predictions_file'].format(project=self.project)

        if os.path.exists(predictions_file):
            self.predictions = pd.read_csv(predictions_file, encoding='utf-8')
        else:
            self._generate_comp_predictions()
            # Store and cache predictions
            self.predictions = self.predictions.sort_values(by=['comp_total'])
            self.predictions.to_csv(
                predictions_file, index=False)

    def _generate_comp_predictions(self):
        """
        Generate computational predictions
        """
        print(f"Generating '{self.project}' predictions ...")
        pbar = tqdm(
            total=len(self.backlog),
            desc=f"{self.project}: Comp Predicting Progress")
        for _, user_story in self.backlog.iterrows():
            m = Metrics(
                project = self.project,
                user_story = user_story['text'],
                usid = user_story['usid'])

            # Calculate metrics
            format_complete = m.run_metric('format_complete')
            readable = m.run_metric('readable')
            customer_speak = m.run_metric('customer_speak')
            small = m.run_metric('small')
            independent = m.run_metric('independent')
            word_sparse = m.run_metric('word_sparse')
            sentence_sparse = m.run_metric('sentence_sparse')
            easy_language = m.run_metric('easy_language')

            new_predictions = pd.DataFrame({
                'usid':user_story['usid'],
                'format_complete':format_complete,
                'readable':readable,
                'customer_speak':customer_speak,
                'small':small,
                'independent':independent,
                'word_sparse':word_sparse,
                'sentence_sparse':sentence_sparse,
                'easy_language':easy_language,
                'comp_total':format_complete + readable + customer_speak + \
                    small + independent + word_sparse + sentence_sparse}, index=[0])

            self.predictions = pd.concat([self.predictions, new_predictions], ignore_index=True)
            pbar.update(1)
        pbar.close()
