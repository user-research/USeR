from metrics.BaseMetric import BaseMetric, config
import numpy as np
import os
import pandas as pd
import string
from sklearn.feature_extraction.text import TfidfVectorizer

class CustomerSpeak(BaseMetric):
    """
    Metric class: customer speak
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Glossary
        self.glossary = []

        # Quality metrics
        self._customer_speak = 0

        # Init glossary
        self._build_glossary()
    
    def run(self):
        """
        Runs the metrics calculation
        """
        return self.customer_speak()

    def get_glossary(self):
        """
        Get glossary
        """
        return self.glossary
    
    def get_glossary_len(self):
        """
        Get glossary length
        """
        return len(self.glossary)

    def customer_speak(self):
        """ 
        Calculates customer_speak quality metric
        """
        # Get user story tokens
        tokens = self.cleaner.spacy_tokenizer_without_ner(self.user_story)
        tokens = tokens + self.cleaner.spacy_ner_tokenizer(self.user_story)

        # Remove duplicates
        unique_tokens = list(set(tokens))
        unique_tokens_len = len(unique_tokens)
        
        # Find story and glossary words intersection
        business_sec_len = len([word for word in unique_tokens if word in self.glossary])
        
        self._customer_speak = 0.0

        if unique_tokens_len != 0:
            # Range 0 - 1; 0 = low quality, 1 = high quality
            self._customer_speak = business_sec_len / unique_tokens_len

        return self._customer_speak
    
    def _build_glossary(self):
        """
        Builds the glossary from the user stories
        """
        glossary_file = config['project']['glossary_file'].format(project=self.project)
        if os.path.exists(glossary_file):
            self.glossary = pd.read_csv(glossary_file).values
        else:
            glossary = self._build_glossary_tfidf() + \
                       self._build_glossary_named() + \
                       self._build_glossary_lemma()
            
            # Remove duplicates
            self.glossary = list(set(glossary))
            
            pd.DataFrame(self.glossary).to_csv(glossary_file, index=False, header=None)

    def _build_glossary_tfidf(self):
        """
        Extracts extential business domain words found in the user stories. Extract words with TFIDF.
        """
        glossary = []

        # Get full backlog
        backlog = self.backlogs.get_backlog(self.project)['text']

        # Get words that have stories in common
        tfidf_vector = TfidfVectorizer(tokenizer=self.cleaner.spacy_tokenizer_without_ner)
        X = tfidf_vector.fit_transform(backlog)
        feature_names = tfidf_vector.get_feature_names_out()

        frequencies = sorted(list(zip(feature_names, X.sum(0).getA1())), key = lambda x: x[1], reverse = True)
        plain_values = [value for _, value in frequencies]

        upper = np.percentile(plain_values, 90)
        glossary = [key for key, value in frequencies if value > upper]
        
        return glossary

    def _build_glossary_named(self):
        """
        Extract named entities.
        """
        glossary = []
        for story in self.backlogs.get_backlog(self.project)['text']:
            ners = self.cleaner.spacy_ner_tokenizer(story)
            for ner in ners:
                glossary.append(ner)
        # Remove duplicates
        glossary = list(set(glossary))

        return glossary

    def _build_glossary_lemma(self):
        """
        Extract words to whom we can not found a lemma.
        """
        glossary = []
        for story in self.backlogs.get_backlog(self.project)['text']:
            # skip ner tokens
            tokens = self.cleaner.get_cleaned_spacy_tokens_without_ner(story)
            for token in tokens:
                text = token.text.lower().strip(string.punctuation)
                lemma = token.lemma_.lower().strip(string.punctuation)
                base = token._.is_base_form_
                # First: lookup if lemma can be found?
                # Second: word isn't in base form, means we found a special one e.g. "Evaluationen"
                if (text == lemma and not base):
                    # Fill missing lemmas
                    glossary.append(lemma)
        # Remove duplicates
        glossary = list(set(glossary))
        
        return glossary