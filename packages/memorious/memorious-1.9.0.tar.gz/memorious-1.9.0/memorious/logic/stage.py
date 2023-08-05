import re
from importlib import import_module
from servicelayer.extensions import get_entry_point

from memorious.model import Crawl


class CrawlerStage(object):
    """A single step in a data processing crawler."""

    def __init__(self, crawler, name, config):
        self.crawler = crawler
        self.name = name
        self.validate_name()
        self.config = config
        self.method_name = config.get("method")
        self.params = config.get("params") or {}
        self.handlers = config.get("handle") or {}

    @property
    def method(self):
        # method A: via a named Python entry point
        func = get_entry_point("memorious.operations", self.method_name)
        if func is not None:
            return func
        # method B: direct import from a module
        if ":" not in self.method_name:
            raise ValueError("Unknown method: %s", self.method_name)
        package, method = self.method_name.rsplit(":", 1)
        module = import_module(package)
        return getattr(module, method)

    def validate_name(self):
        if not re.match(r"^[A-Za-z0-9_-]+$", self.name):
            raise ValueError(
                "Invalid stage name: %s. " "Allowed characters: A-Za-z0-9_-" % self.name
            )

    @property
    def op_count(self):
        """Total operations performed for this stage"""
        return Crawl.op_count(self.crawler, self)

    @property
    def namespaced_name(self):
        return "{0}.{1}".format(self.crawler, self.name)

    @classmethod
    def detach_namespace(self, namespaced_name):
        return namespaced_name.split(".")[-1]

    def __str__(self):
        return self.name

    def __repr__(self):
        return "<CrawlerStage(%r, %s)>" % (self.crawler, self.name)
