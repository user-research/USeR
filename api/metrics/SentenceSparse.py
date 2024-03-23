from metrics.BaseMetric import BaseMetric

class SentenceSparse(BaseMetric):
    """
    Metric class: sentence sparse
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Quality metric
        self._sentence_sparse = 0

    def run(self):
        """
        Runs the metrics calculation
        """
        return self.sentence_sparse()

    def sentence_sparse(self):
        """ 
        Calculates the distance in percentage between 0 and 1 between the mean number of sentences 
        of the user stories in the backlog and the sentence count of the current user story
        """
        doc = self.nlp(self.user_story)
        num_sentences = len(list(doc.sents))
       
        stats = self._get_text_statistics()
        min_sentences = int(stats['min_sentence_count'].iloc[0])
        mean_sentences = int(stats['mean_sentence_count'].iloc[0])
        max_sentences = int(stats['max_sentence_count'].iloc[0])

        # y = ax+b
        # range 0 - 1
        w = min_sentences

        if num_sentences > mean_sentences:
            w = max_sentences

        if (num_sentences > max_sentences) or (num_sentences < min_sentences) or (mean_sentences == w):
            self._sentence_sparse = 0.0

            return self._sentence_sparse

        self._sentence_sparse = (num_sentences - w) / (mean_sentences - w)

        return self._sentence_sparse