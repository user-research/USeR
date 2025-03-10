import hashlib
from metrics.base_metric import BaseMetric, config
import numpy as np
import os
import pandas as pd

class Independent(BaseMetric):
    """
    Metric class: independent
    """
    def __init__(self, *args, **kwargs):
        """
        Initialize the independent metric class

        Args:
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments
        """
        super().__init__(*args, **kwargs)

        # Quality metric
        self._independent = 0.0

    def run(self) -> float:
        """
        Runs the metrics calculation

        Returns:
            float: The independent metric
        """
        return self.independent()

    def independent(self) -> float:
        """
        Calculates the independent metric. It uses the user story and 
        the backlog to calculate the cosine similarity.

        Returns:
            float: The independent metric
        """
        cache_file = config['project']['independent_file'].format(project=self.project)

        independent_cache_entries = []
        m = hashlib.sha256(self.user_story.encode('UTF-8'))
        story_hash = m.hexdigest()

        if os.path.exists(cache_file):
            independent_cache_entries = pd.read_csv(cache_file, header=None).values.tolist()
            for tmp_hash, self._independent in independent_cache_entries:
                if tmp_hash == story_hash:
                    return self._independent

        similarities = []
        search_doc = self.nlp(self.user_story)

        for _, story in self.backlogs.get_backlog(self.project).iterrows():
            main_doc = self.nlp(story['text'])
            similarity_value = main_doc.similarity(search_doc)
            similarities.append(similarity_value)

        # Inverse value; Range 0 - 1; 0 = low independent, 1 = high independent
        self._independent = 1 - np.average(similarities)

        # Cache
        if config.getboolean('app', 'cache'):
            independent_cache_entries.append([story_hash, self._independent])
            pd.DataFrame(independent_cache_entries).to_csv(cache_file, index=False, header=None)

        return self._independent
