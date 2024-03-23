from config.user.UserConfigParser import config
from metrics.Metrics import Metrics
import itertools as it
import math
import numpy as np
import os
import pandas as pd
import scipy.stats as scst
from stats.BaseStats import BaseStats
from tqdm import tqdm

# https://stackoverflow.com/questions/25351968/how-to-display-full-non-truncated-dataframe-information-in-html-when-convertin
pd.set_option('display.max_colwidth', None)

from collections import defaultdict
# Utility function to create dictionary
# https://www.geeksforgeeks.org/python-creating-multidimensional-dictionary/
def multi_dict(K, type):
    """
    Create a multi-dimensional dictionary
    """
    if K == 1:
        return defaultdict(type)
    else:
        return defaultdict(lambda: multi_dict(K-1, type))

class ProjectStats(BaseStats):
    """
    ProjectStats class
    """
    def __init__(self, project="p1"):
        super().__init__(setting='project', project=project)

        # Add user story ids to whom we want to predict the quality
        self.usids = pd.read_csv(
            config[self.setting]['usids_file'].format(project=self.project), encoding='utf-8')

        # Add the full corpus to query user stories
        self.corpus = pd.read_csv(
            config[self.setting]['corpus_file'].format(project=self.project), encoding='utf-8')

    def generate_predictions(self):
        """
        Generate predictions for a project
        """
        predictions_file = config[self.setting]['predictions_file'].format(project=self.project)

        if os.path.exists(predictions_file):
            self.predictions = pd.read_csv(predictions_file, encoding='utf-8')
        else:
            self._generate_comp_predictions()
            self._add_likert_scale_expert_predictions()
            # Uncomment to add user story text to predictions
            #self._add_story_text()

            # Store and cache predictions
            self.predictions = self.predictions.sort_values(by=['comp_total'])
            self.predictions.to_csv(
                predictions_file, index=False)

    def _generate_comp_predictions(self):
        """
        Generate computational predictions
        """
        pbar = tqdm(
            total=len(self.usids),
            desc=f"{self.project}: Comp Predicting Progress")
        for _,usid in enumerate(self.usids['usid']):
            user_story = self.corpus.loc[self.corpus['usid'] == usid]
            if user_story.empty:
                continue

            user_story = user_story['text'].to_string(index = False)
            m = Metrics(project = self.project, user_story = user_story, usid = usid)

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
                'usid':usid,
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

    def _add_likert_scale_expert_predictions(self):
        """
        Add the likert scale expert ratings to join their ratings to computational results
        """
        experts = pd.read_csv(
            config[self.setting]['experts_file'].format(project=self.project),encoding='utf-8')

        self.predictions['expert_rating'] = math.nan

        for idx, prediction in self.predictions.iterrows():
            # Likert-scale rating
            expert_entry = experts.loc[experts['usid'] == prediction['usid']]
            if expert_entry.empty:
                continue

            self.predictions.at[idx, 'expert_rating'] = expert_entry['rating_median']

    def _add_story_text(self):
        """
        Add the user story text to predictions to better interpret metrics values related to the story text
        """
        self.predictions['user_story'] = ''

        for idx, _ in self.predictions.iterrows():
            user_story = self.corpus.loc[self.corpus['usid'] == self.predictions.loc[idx]['usid']]
            self.predictions.at[idx, 'user_story'] = user_story['text'].to_string(index = False)