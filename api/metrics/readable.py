from metrics.base_metric import BaseMetric
import textstat

class Readable(BaseMetric):
    """
    Metric class: readable
    """
    def __init__(self, *args, **kwargs):
        """
        Initialize the readable metric class

        Args:
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments
        """
        super().__init__(*args, **kwargs)

        # Quality metrics
        self._readable = 0.0

    def run(self) -> float:
        """
        Runs the metrics calculation
        """
        return self.readable()

    def readable(self) -> float:
        """ 
        Calculates the lexial quality based on flesch readability metric

        Returns:
            float: The readability quality
        """
        textstat.set_lang("de_DE")
        # Range for de -inf to 180; -inf = low quality, 180 = high quality
        # Zero string '' to get 180 as max szenario
        max_flesch = textstat.flesch_reading_ease(r'')
        flesch = textstat.flesch_reading_ease(self.user_story)
        # Prevent negative readability
        flesch = 0 if (flesch < 0) else flesch

        self._readable =  flesch / max_flesch

        return self._readable
