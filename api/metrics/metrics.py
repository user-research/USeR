from metrics.metrics_registry import MetricsRegistryBase
from metrics.customer_speak import CustomerSpeak
from metrics.easy_language import EasyLanguage
from metrics.format_complete import FormatComplete
from metrics.independent import Independent
from metrics.readable import Readable
from metrics.sentence_sparse import SentenceSparse
from metrics.small import Small
from metrics.word_sparse import WordSparse

# https://charlesreid1.github.io/python-patterns-the-registry.html
class Metrics:
    """
    Metrics container class for all metrics instances 
    to perform all metrics calculation at once.
    """
    def __init__(self, *args, **kwargs):
        """
        Initialize the metrics container class

        Args:
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments
        """
        # Store instances of each doctype
        self.all_metrics = {}

        # Iterate over every metric
        for metrics_name, metrics_class in MetricsRegistryBase.METRICS_REGISTRY.items():

            # Create an instance of type doctype_class
            metrics_instance = metrics_class(*args, **kwargs)

            # Save for later
            self.all_metrics[metrics_name] = metrics_instance

    def run(self) -> dict:
        """
        Start the metrics calculation for all metrics

        Returns:
            dict: The results of all metrics
        """
        results = {}
        for metrics_name, metric_instance in self.all_metrics.items():
            results[metrics_name] = metric_instance.run()

        return results

    def run_metric(self, search_metric_name) -> float:
        """
        Start the metrics calculation for a specific metric

        Args:
            search_metric_name (str): The name of the metric to run

        Returns:
            float: The result of the specific metric

        Raises:
            NotImplementedError: If the metric is not found
        """
        for metric_name, metric_instance in self.all_metrics.items():
            if  metric_name == search_metric_name:
                return metric_instance.run()

        raise NotImplementedError(f"Metric '{search_metric_name}' not found!")

    def get_metric(self, search_metric_name: str) -> object:
        """
        Get the instance of a specific metric

        Args:
            search_metric_name (str): The name of the metric to get

        Returns:
            BaseMetric: The instance of the specific metric

        Raises:
            NotImplementedError: If the metric is not found
        """
        for metric_name, metric_instance in self.all_metrics.items():
            if metric_name == search_metric_name:
                return metric_instance

        raise NotImplementedError(f"Metric '{search_metric_name}' not found!")
