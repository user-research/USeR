from bertopic import BERTopic
import hashlib
from metrics.base_metric import BaseMetric, config, logging
import numpy as np
import os
import pandas as pd
import scipy.stats as stats
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import TfidfVectorizer

class Small(BaseMetric):
    """
    Metric class: small
    """
    def __init__(self, *args, **kwargs):
        """
        Initialize the small metric class

        Args:
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments
        """
        super().__init__(*args, **kwargs)

        # Contains the topic model trained for the small metric
        self.topic_model = None

        # Quality metric
        self._small = 0.0

        # Init small metric training
        self._train_small()

    def run(self) -> float:
        """
        Runs the metrics calculation

        Returns:
            float: The small metric
        """
        return self.small()

    def get_topic_model(self) -> BERTopic:
        """
        Get the topic model

        Returns:
            BERTopic: The topic model
        """
        return self.topic_model

    def _spacy_tokenizer(self, sentence: str) -> list:
        """
        Tokenizer function used in model training

        Args:
            sentence: Sentence to be tokenized

        Returns:
            Text tokens
        """
        tokens = self.cleaner.spacy_tokenizer(
            sentence=sentence, remove_stop_words=False)

        # return preprocessed list of tokens
        return tokens

    def _train_small(self) -> BERTopic:
        """
        Training method for small criteria and topic modeling.

        Returns:
            BERTopic: The trained
        """
        # https://spacy.io/universe/project/bertopic
        # https://maartengr.github.io/BERTopic/index.html
        # Support multilingual model for German

        # Use full backlog to optimize topic modelling by sharper 
        # spliting default and context topics
        backlog = self.backlogs.get_backlog(self.project)['text'].tolist()

        # Use spaCy tokenizer for German
        vectorizer = TfidfVectorizer(tokenizer=self._spacy_tokenizer)

        # Chosen embedding model for German
        # https://huggingface.co/aari1995/German_Semantic_STS_V2
        chosen_embedding_model = 'aari1995/German_Semantic_STS_V2'
        embedding_model = SentenceTransformer(
            chosen_embedding_model,
            cache_folder=config['app']['cache_folder'])

        topic_model = BERTopic(
            embedding_model=embedding_model,
            # decrease the number of min topics 10 -> 3 detection to work 
            # with fewer data sets < ~1000
            min_topic_size=3,
            vectorizer_model=vectorizer,
            calculate_probabilities=True,
            verbose=True)

        bert_cache_file = config['project']['bert_cache_file'].format(project=self.project)

        if os.path.exists(bert_cache_file):
            best = BERTopic.load(
                bert_cache_file,
                embedding_model=chosen_embedding_model)
        else:
            try:
                topic_model.fit(backlog)
            except TypeError:
                logging.error('Failure in predicting BERTopic model.')
            best = topic_model

            best.save(
                bert_cache_file,
                save_embedding_model=False)

        self.topic_model = best

        # Get topic infors (topics and distributions)
        # Store visualizaton of topics to allow a better handling
        try:
            show_topics_file = config['project']['show_topics_file'].format(project=self.project)
            if not os.path.exists(show_topics_file):
                topic_info = self.topic_model.visualize_topics()
                html = topic_info.to_html()
                func = open(show_topics_file, "w", encoding='utf-8')
                func.write(html)
                func.close()
        except Exception as e:
            logging.error(e)

        try:
            # Hierarchical structure
            show_hierarchical_topics_file = \
                config['project']['show_hierarchical_topics_file'].format(project=self.project)
            if not os.path.exists(show_hierarchical_topics_file):
                hierarchical_topics = self.topic_model.hierarchical_topics(backlog)
                html = self.topic_model.visualize_hierarchy(
                    hierarchical_topics=hierarchical_topics).to_html()
                func = open(show_hierarchical_topics_file, "w", encoding='utf-8')
                func.write(html)
                func.close()
        except Exception as e:
            logging.error(e)

        try:
            show_tree_topics_file = \
                config['project']['show_tree_topics_file'].format(project=self.project)
            if not os.path.exists(show_tree_topics_file):
                html = self.topic_model.get_topic_tree(hierarchical_topics)
                func = open(show_tree_topics_file, "w", encoding='utf-8')
                func.write(html)
                func.close()
        except Exception as e:
            logging.error(e)

        return self.topic_model

    def small(self) -> float:
        """
        Predict small quality metric based on topic model.

        Returns:
            float: The small metric
        """
        # Cache settings
        cache_file = config['project']['small_file'].format(project=self.project)
        probs_cache_file = config['project']['small_probs_file'].format(project=self.project)
        small_cache_entries = []

        m = hashlib.sha256(
            (self.usid if not self.usid is None else '' + self.user_story).encode('UTF-8'))
        story_hash = m.hexdigest()

        if os.path.exists(cache_file):
            small_cache_entries = pd.read_csv(cache_file, header=None).values.tolist()
            for tmp_hash, self._small in small_cache_entries:
                if tmp_hash == story_hash:
                    return self._small

        try:
            # Predict topics of the backlog/project a user stories belongs to
            if self.topic_model is None:
                self._train_small()
            _, probs = self.topic_model.transform([self.user_story])
            probs = probs[0]
            probs = -np.sort(-probs)

            min_topics = 1
            max_topics = len(probs)

            entry = [self.usid] + probs.tolist()
            pd.DataFrame([entry]).to_csv(
                probs_cache_file, index=False, header=None, mode='a')

            # Run Generalized ESD Test for Outliers to detect outlier
            # probabilities that are topic related
            num_topics = esd_test(probs, 0.05, 10)

            # In case of only one topic was found by BERTopic, we assume the
            # story contains just this single topic
            if (max_topics - min_topics) == 0:
                self._small = 1.0
            # If we couldn't find outliers, we assume two cases:
            elif num_topics == 0:
                # The story contains/opens a new topic which not releates to existing topics,
                # shown by low probabilities to all topics
                self._small = 1.0
                # The story is related to almost all topics, shown by high probabilities
                # to all topics
                if np.mean(probs) > 0.5 and np.std(probs) < 0.1:
                    self._small = 0.0
            else:
                # Inverse value; Range 0 - 1; 0 = low quality, 1 = high quality
                self._small = 1 - (num_topics - min_topics) / (max_topics - min_topics)

            # Cache
            if config.getboolean('app', 'cache'):
                pd.DataFrame([[story_hash, self._small]]).to_csv(
                    cache_file, index=False, header=None, mode='a')
        except Exception as e:
            logging.error(e)

        return self._small

# Generalized Extreme Studentized Deviate (ESD) Test is a statistical test for outliers
# https://www.itl.nist.gov/div898/handbook/eda/section3/eda35h3.htm
# https://github.com/bhattbhavesh91/outlier-detection-grubbs-test-and-generalized-esd-test-python/blob/master/generalized-esd-test-for-outliers.ipynb
def _grubbs_stat(y: list) -> float:
    """
    Calculate the Grubbs Statistics Value

    Args:
        y: The input data

    Returns:
        float: The Grubbs Statistics
    """
    std_dev = np.std(y)
    avg_y = np.mean(y)
    abs_val_minus_avg = abs(y - avg_y)
    max_of_deviations = max(abs_val_minus_avg)
    max_ind = np.argmax(abs_val_minus_avg)
    gcal = max_of_deviations/ std_dev
    print(f"Grubbs Statistics Value : {gcal}")

    return gcal, max_ind

def _calculate_critical_value(size: int, alpha: float) -> float:
    """
    Calculate the critical value for the Grubbs Test

    Args:
        size: The size of the input data
        alpha: The significance level

    Returns:
        float: The critical value
    """
    t_dist = stats.t.ppf(1 - alpha / (2 * size), size - 2)
    numerator = (size - 1) * np.sqrt(np.square(t_dist))
    denominator = np.sqrt(size) * np.sqrt(size - 2 + np.square(t_dist))
    critical_value = numerator / denominator
    print(f"Grubbs Critical Value: {critical_value}")

    return critical_value

def _check_g_values(gs: float, gc: float, inp: dict, max_index: int) -> int:
    """
    Check if the calculated G-statistic is greater than the critical value
    """
    if gs > gc:
        print(f'{inp[max_index]} is an outlier. G > G-critical: {gs:.4f} > {gc:.4f} \n')
        return 1
    else:
        print(f'{inp[max_index]} is not an outlier. G > G-critical: {gs:.4f} > {gc:.4f} \n')
        return 0

def esd_test(input_series: list, alpha: float, max_outliers: int) -> int:
    """
    Generalized Extreme Studentized Deviate (ESD) Test is a statistical test for outliers

    Args:
        input_series: The input data
        alpha: The significance level
        max_outliers: The maximum number of outliers

    Returns:
        int: The number of outliers
    """
    outliers = 0
    # Generalized Extreme Studentized Deviate (ESD)
    for _ in range(max_outliers):
        if np.std(input_series) == 0:
            break
        gcritical = _calculate_critical_value(len(input_series), alpha)
        gstat, max_index = _grubbs_stat(input_series)
        outliers += _check_g_values(gstat, gcritical, input_series, max_index)
        input_series = np.delete(input_series, max_index)

    print(f"Number of outliers: {outliers}")

    return outliers
