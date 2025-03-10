from metrics.base_metric import BaseMetric

class WordSparse(BaseMetric):
    """
    Metric class: word sparse
    """
    def __init__(self, *args, **kwargs):
        """
        Initialize the word sparse metric class

        Args:
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments
        """
        super().__init__(*args, **kwargs)

        # Quality metric
        self._word_sparse = 0.0

    def run(self) -> float:
        """
        Runs the metrics calculation

        Returns:
            float: The word sparse metric
        """
        return self.word_sparse()

    def word_sparse(self) -> float:
        """ 
        Calculates the distance in percentage between 0 and 1 between the mean number of words 
        of the user stories in the backlog and the word count of the current user story

        Returns:
            float: The word sparse metric
        """
        doc = self.nlp(self.user_story)
        num_words = len(doc)

        stats = self._get_text_statistics()
        min_words = int(stats['min_word_count'].iloc[0])
        mean_words = int(stats['mean_word_count'].iloc[0])
        max_words = int(stats['max_word_count'].iloc[0])

        # y = ax+b
        # range 0 - 1
        w = min_words

        if num_words > mean_words:
            w = max_words

        if (num_words > max_words) or (num_words < min_words) or (mean_words == w):
            self._word_sparse = 0.0

            return self._word_sparse

        self._word_sparse = (num_words - w) / (mean_words - w)

        return self._word_sparse
