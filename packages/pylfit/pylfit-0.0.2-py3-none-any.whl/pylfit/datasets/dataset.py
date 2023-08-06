#-----------------------
# @author: Tony Ribeiro
# @created: 2020/12/23
# @updated: 2021/01/13
#
# @desc: Interface class of LFIT datasets
#   - Features/target variables labels and domain
#   - State values are encode by their value id
#-----------------------

from ..utils import eprint

import abc

class Dataset():
    """ Abstract class of LFIT algorithm input datasets

    """

    """ Feature variables name and domain: list of pair (string, list of string) """
    _features = []

    """ Target variables name and domain: list of pair (string, list of string) """
    _targets = []

    """ Dataset class must implement a data attribute """
    #_data = []

#--------------
# Constructors
#--------------

    def __init__(self, features, targets):
        """
        Constructor of an empty dataset

        Args:
            features: list of pair (string, list of objects)
                Feature variables name and domain
            targets: list of pair (string, list of objects)
                Target variables name and domain
        """

        self.features = features
        self.targets = targets

#--------------
# Operators
#--------------

    def __str__(self):
        return self.to_string()

    def __repr__(self):
        return self.to_string()

    @abc.abstractmethod
    def fit(self, dataset):
        """

        """
        raise NotImplementedError('Must be implemented in subclasses.')

    @abc.abstractmethod
    def to_string(self):
        """
        Convert the object to a readable string

        Returns:
            String
                a readable representation of the object
        """
        raise NotImplementedError('Must be implemented in subclasses.')

#--------------
# Accessors
#--------------

    @property
    def features(self):
        return self._features

    @features.setter
    def features(self, value):
        self._features = value

    @property
    def targets(self):
        return self._targets

    @targets.setter
    def targets(self, value):
        self._targets = value
