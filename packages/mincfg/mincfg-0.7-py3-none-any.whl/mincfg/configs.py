"""
Configurations are the way that multiple sources are glommed together.

MergedConfiguration merges multiple sources linearly, with later sources taking precedence over earlier ones.

"""

import logging
from types import SimpleNamespace
from typing import Dict, List, Optional

from .sources import ConfigSource, CfgDict

logger = logging.getLogger(__name__)


def _recursive_dict_update(main: Dict, update: Dict):
    """
    like dict.update(), modifies the 'main' by applying 'update'
    UNLIKE dict.update(), normalizes all keys to lowercase
    :meta private:
    """
    for k, v in update.items():
        lk = k.lower()
        if isinstance(v, dict):
            main[lk] = main.get(lk, dict())
            logger.debug("dict %r %s recursing into dict %r to write %r", id(main), lk, id(main[lk]), v)
            _recursive_dict_update(main[lk], v)
        else:
            logger.debug("dict %r : %s -> %r", id(main), lk, v)
            main[lk] = v


class MergedConfiguration:
    """
    Merges configuration sources

    :param sources: a list of :ref:ConfigSource objects to merge, with later ones overriding earlier ones
    """
    def __init__(self, sources: Optional[List[ConfigSource]] = None):
        self.sources: List[ConfigSource] = [] if sources is None else sources
        self._cfg: Optional[CfgDict] = None

    def __repr__(self):
        return 'MergedConfiguration([' + ', '.join(repr(s) for s in self.sources) + ')'

    def add_source(self, source: ConfigSource):
        self.sources.append(source)
        self._cfg = None

    def load(self):
        """
        Cause the config to be loaded; note that this need not be called directly, as it is lazily loaded.
        Subsequent calls _will_ re-load from the config sources.
        """
        cfg: CfgDict = dict()
        for source in self.sources:
            updates = source.as_dict()
            _recursive_dict_update(cfg, updates)
        self._cfg = cfg

    def as_dict(self, namespace: Optional[List[str]] = None) -> CfgDict:
        """
        return the configuration, or a namespace within it, as a single dictionary

        :param namespace: the namespace to return as a dict.  If unspecified, return the entire config.
        """
        if self._cfg is None:
            self.load()
        ns = [] if namespace is None else namespace
        assert self._cfg is not None
        in_ns = self._cfg
        for subns in ns:
            in_ns = in_ns.setdefault(subns, dict())
        if not isinstance(in_ns, dict):
            raise ValueError(f"namespace {'.'.join(ns)} points to a key, not a dict")
        return in_ns

    def get(self, key: str, namespace: Optional[List[str]]=None, default=None, parser=str, raise_error=True, doc=None):
        """
        get a single config key

        :param namespace: the 'path' in the config to the namespace to look the key up in
        :param default: is the value to use if the key is not found
        :param parser: is how to cast the result
        :param raise_error: is whether to raise an error if the key is not found (note: supplying a default negates
            raise_error, as a (presumably) valid value is always available)
        :param doc: is extra information to supply with the error message
        """
        k = key.lower()
        ns = namespace or []
        in_ns = self.as_dict()
        for subns in ns:
            in_ns = in_ns[subns]
        if raise_error and default is None and k not in in_ns:
            msg = f"Missing config key {'.'.join(ns + [k])}"
            if doc:
                msg += f": {doc}"
            raise KeyError(msg)
        return parser(in_ns.get(k, default))

    def as_ns(self, namespace: List[str]) -> SimpleNamespace:
        """
        return the config, or a namespace within it, as a SimpleNamespace

        :param namespace: the namespace to return as a SimpleNamespace.  If unspecified, return the entire config.
        """
        return SimpleNamespace(**self.as_dict(namespace))
