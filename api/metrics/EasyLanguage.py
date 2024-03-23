from metrics.BaseMetric import BaseMetric, config
import pandas as pd

class EasyLanguage(BaseMetric):
    """
    Metric class: word sparse
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Quality metric
        self._word_sparse = 0
    
    def run(self):
        """
        Runs the metrics calculation
        """
        return self.easy_language()
    
    def easy_language(self):
        """
        Calculates the easy language metric. It uses a list of basic/easy language words and 
        the tokens of the current user story to build an intersection. As a second step it calculates the ratio
        between the intersected words and the total story words
        """
        # https://zsl-bw.de/,Lde/Startseite/allgemeine-bildung/grundwortschatz-deutsch-gs
        # School class 1. - 4.
        base_words_de = list(
            pd.read_csv(config['lists.de']['basic_words'], header=None).values.reshape(-1))

        # Lemmatizing each token and converting each token into lowercase
        tokens = self.cleaner.spacy_tokenizer(
            self.user_story, remove_stop_words=False)
        
        # Remove duplicates
        unique_tokens = set(tokens)
        unique_tokens_len = len(unique_tokens)

        # Find story and base words intersection
        base_sec_len = len([word for word in unique_tokens if word in base_words_de])
        
        self._word_sparse = 0.0

        if unique_tokens_len != 0:
             # Range 0.0 - 1.0; 0.0 = low quality, 1.0 = high quality
            self._word_sparse = base_sec_len / unique_tokens_len

        return self._word_sparse