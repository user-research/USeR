from metrics.MetricsRegistry import MetricsRegistryBase
from metrics.CustomerSpeak import CustomerSpeak
from metrics.EasyLanguage import EasyLanguage
from metrics.FormatComplete import FormatComplete
from metrics.Independent import Independent
from metrics.Readable import Readable
from metrics.SentenceSparse import SentenceSparse
from metrics.Small import Small
from metrics.WordSparse import WordSparse

# https://charlesreid1.github.io/python-patterns-the-registry.html
class Metrics(object):
    """
    Metrics container class for all metrics instances 
    to perform all metrics calculation at once.
    """
    def __init__(self, *args, **kwargs):

        # Store instances of each doctype
        self.all_metrics = {}

        # Iterate over every metric
        for metrics_name, metrics_class in MetricsRegistryBase.METRICS_REGISTRY.items():
 
            # Create an instance of type doctype_class  
            metrics_instance = metrics_class(*args, **kwargs)

            # Save for later
            self.all_metrics[metrics_name] = metrics_instance

    def run(self):
        """
        Start the metrics calculation for all metrics
        """
        results = {}
        for metrics_name, metric_instance in self.all_metrics.items():
            results[metrics_name] = metric_instance.run()
        return results
    
    def run_metric(self, search_metric_name):
        """
        Start the metrics calculation for a specific metric
        """
        for metric_name, metric_instance in self.all_metrics.items():
            if  metric_name == search_metric_name:
                return metric_instance.run()
    
    def get_metric(self, search_metric_name):
        """
        Get the instance of a specific metric
        """
        for metric_name, metric_instance in self.all_metrics.items():
            if metric_name == search_metric_name:
                return metric_instance