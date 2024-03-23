from functools import reduce
from config.user.UserConfigParser import config

# https://charlesreid1.github.io/python-patterns-the-registry.html
class MetricsRegistryBase(type):
    """
    Metaclass for registering metrics classes
    """
    # Holds all configured metric instances
    METRICS_REGISTRY = {}

    def __new__(cls, name, bases, attrs):
        # Instantiate a new type corresponding to the type of class being defined
        # this is currently RegisterBase but in child classes will be the child class
        new_cls = type.__new__(cls, name, bases, attrs)
        metric_str = reduce(lambda x, y: x + ('_' if y.isupper() else '') + y.lower(), new_cls.__name__).lower()
        
        # Only add valid metrics to registry
        default_metrics = config['app']['metrics'].split(r',')
        if metric_str in default_metrics:
            cls.METRICS_REGISTRY[metric_str] = new_cls
        
        return new_cls

    @classmethod
    def get_metrics_registry(cls):
        return dict(cls.METRICS_REGISTRY)

# https://github.com/faif/python-patterns/blob/master/patterns/behavioral/registry.py
class BaseRegisteredClass(metaclass=MetricsRegistryBase):
    """
    Any class that will inherits from BaseRegisteredClass will be included
    inside the dict RegistryHolder.REGISTRY, the key being the name of the
    class and the associated value, the class itself.
    """
    pass