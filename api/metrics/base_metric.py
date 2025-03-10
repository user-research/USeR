from config.config_parser import config
from helper.cleaner import Cleaner
from helper.backlog import Backlog
import logging as logging
from metrics.metrics_registry import BaseRegisteredClass
import numpy as np
import os
import pandas as pd
import spacy
from spacy.lang.de import German
from spacy.tokens import Token
from spacy.tokens import Doc

logging.basicConfig(filename=config['app']['sys_log_file'], filemode='w', level=logging.ERROR)

# https://spacy.io/usage/processing-pipelines#custom-components
@German.factory("base_form_lemmatizer")
class BaseFormLemmatizer:
    """
    Custom spaCy pipeline component to determine if a token is a base form.
    """
    def __init__(self, nlp: German, name: str, label: str="BFL"):
        """
        Initialize the custom pipeline component.

        Args:
            nlp (Language): The shared nlp object.
            name (str): The component name.
            label (str): The component label.
        """
        Token.set_extension("is_base_form_", default=None)

    def __call__(self, doc: Doc) -> Doc:
        """
        Process the text and set the custom extension.

        Args:
            doc (Doc): The Doc object in the pipeline.

        Returns:
            Doc: The Doc object with the custom extension set.
        """
        for token in doc:
            token._.set("is_base_form_", self.is_base_form(token))

        return doc

    # Adopted from english version until german version is available
    # see: https://github.com/explosion/spaCy/blob/master/spacy/lang/en/lemmatizer.py
    def is_base_form(self, token: Token) -> bool:
        """
        Check whether we're dealing with an uninflected paradigm, so we can
        avoid lemmatization entirely.

        Args:
            token (Token): The token to check.

        Returns:
            bool: Whether the token is a base form.
        """
        # univ_pos (unicode / int): The token's universal part-of-speech tag.
        univ_pos = token.pos_.lower()
        # morphology (dict): The token's morphological features following the
        #    Universal Dependencies scheme.
        #    See for german: https://universaldependencies.org/de/index.html
        morphology = token.morph.to_dict()

        if univ_pos == "noun" and morphology.get("Number") == "Sing":
            return True
        elif univ_pos == "verb" and morphology.get("VerbForm") == "Inf":
            return True
        # This maps 'VBP' to base form -- probably just need 'IS_BASE'
        # morphology
        elif univ_pos == "verb" and (
            morphology.get("VerbForm") == "Fin"
            and morphology.get("Tense") == "Pres"
            and morphology.get("Number") is None
        ):
            return True
        elif univ_pos == "adj" and morphology.get("Degree") == "Pos":
            return True
        elif morphology.get("VerbForm") == "Inf":
            return True
        elif morphology.get("VerbForm") == "None":
            return True
        elif morphology.get("Degree") == "Pos":
            return True
        else:
            return False

class BaseMetric(BaseRegisteredClass):
    """
    Base metrics class for all metrics calculation.
    """
    # https://explosion.ai/blog/german-model
    # Load German tokenizer, tagger, parser, NER and word vectors
    nlp = spacy.load(config['ai']['spacy_model'])
    # Add german (adopted from english) base form lemmatizer
    nlp.add_pipe("base_form_lemmatizer")
    # Load all user stories
    backlogs = Backlog()
    # Cleaning and tokenizing text
    cleaner = Cleaner()

    def __init__(self, project: str="p1", user_story: str="", usid: str=None):
        """
        Initialize the base metric class

        Args:
            project (str): The project name
            user_story (str): The user story text
            usid (str): The user story id
        """
        # Backlog,-length and user story ids vec to select stories
        self.project = project

        # User story text and id
        self.user_story = self.cleaner.convert_and_clean(user_story)
        self.usid = usid

    def run(self):
        """
        Runs the metrics calculation

        Raises:
            NotImplementedError: Implement me in subclass
        """
        raise NotImplementedError('Implement me in subclass')

    def _spacy_tokenizer(self, sentence: str) -> list:
        """
        Tokenizer function used in model training

        Args:
            sentence (str): The sentence to tokenize

        Returns:
            list: List of tokens
        """
        tokens = self.cleaner.spacy_tokenizer(sentence=sentence)

        # return preprocessed list of tokens
        return tokens

    def _get_text_statistics(self) -> pd.DataFrame:
        """
        Helper to retrieve the calculated text statistics of the user stories in a backlog

        Returns:
            pd.DataFrame: The text statistics
        """
        statistics_file = config['project']['backlog_statistics'].format(project=self.project)

        if not os.path.exists(statistics_file):
            self._calc_text_statistics()

        statistics = pd.read_csv(statistics_file, encoding='utf-8')

        return statistics

    def _calc_text_statistics(self):
        """
        Helper to calculates the maximal sentence count of a user story in a backlog
        """
        word_counts = []
        sentence_counts = []

        for _, story in self.backlogs.get_backlog(self.project).iterrows():
            doc = self.nlp(story['text'])
            word_counts.append(len(doc))
            sentence_counts.append(len(list(doc.sents)))

        statistics_file = config['project']['backlog_statistics'].format(project=self.project)

        pd.DataFrame({'backlog_length':len(self.backlogs.get_backlog(self.project)),
                      'min_word_count':np.min(word_counts),
                      'mean_word_count':np.mean(word_counts),
                      'max_word_count':np.max(word_counts),
                      'min_sentence_count':np.min(sentence_counts),
                      'mean_sentence_count':np.mean(sentence_counts),
                      'max_sentence_count':np.max(sentence_counts),}, index=[0]).to_csv(
                          statistics_file, index=False)
