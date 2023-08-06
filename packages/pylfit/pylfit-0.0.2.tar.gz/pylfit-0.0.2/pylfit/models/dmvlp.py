#-------------------------------------------------------------------------------
# @author: Tony Ribeiro
# @created: 2019/03/24
# @updated: 2019/05/03
#
# @desc: class LogicProgram python source code file
#-------------------------------------------------------------------------------

from ..models.model import Model

from ..utils import eprint
from ..objects.rule import Rule

from ..datasets import StateTransitionsDataset

from ..algorithms.gula import GULA

from ..semantics import Synchronous
from ..semantics import Asynchronous

import itertools
import random
import numpy

class DMVLP(Model):
    """
    Define a Dynamic Multi-Valued Logic Program (DMVLP), a set of rules over features/target variables/values
    that can encode the dynamics of a discrete dynamic system (also work for static systems).

    Args:
        features: list of (string, list of string).
            Variables and their values that appear in body of rules
        targets: list of (string, list of string).
            Variables that appear in body of rules.
        rules: list of pylfit.objects.Rule.
            Logic rules of the program.
        algorithm: pyflfit.algorithm.Algorithm subclass.
            The algorithm to be used for fiting the model.
    """


    """ Dataset types compatible with dmvlp """
    _COMPATIBLE_DATASETS = [StateTransitionsDataset]

    """ Learning algorithms that can be use to fit this model """
    _ALGORITHMS = ["gula", "pride", "lf1t"]

    """ Optimization """
    _OPTIMIZERS = []

#--------------
# Constructors
#--------------

    def __init__(self, features, targets, rules=[]):
        """
        Create a DMVLP instance from given features/targets variables and optional rules

        Args:
            features: list of pairs (String, list of String),
                labels of the features variables and their values (appear only in body of rules and constraints).
            targets: list of pairs (String, list of String),
                labels of the targets variables and their values (appear in head of rules and body of constraint).
            rules: list of Rule,
                rules that define logic program dynamics: influences of feature variables values over target variables values.
            name: String,
                the name of the model.
        """
        super().__init__()

        self.features = features
        self.targets = targets
        self.rules = rules

#--------------
# Operators
#--------------

    def __str__(self):
        return self.to_string()

    def _repr__(self):
        return self.to_string()

#--------------
# Methods
#--------------

    def compile(self, algorithm="gula"):
        """
        Set the algorithm to be used to fit the model.
        Supported algorithms:
            - "gula", General Usage LFIT Algorithm (TODO)
            - "pride", (TODO)
            - "lf1t", (TODO)

        """

        if algorithm not in DMVLP._ALGORITHMS:
            raise ValueError('algorithm parameter must be one element of DMVLP._COMPATIBLE_ALGORITHMS: '+str(DMVLP._ALGORITHMS)+'.')

        if algorithm == "gula":
            self.algorithm = GULA
        else:
            raise NotImplementedError('<DEV> algorithm="'+str(algorithm)+'" is in DMVLP._COMPATIBLE_ALGORITHMS but no behavior implemented.')

    def fit(self, dataset):
        """
        Use the algorithm set by compile() to fit the rules to the dataset.
            - Learn a model from scratch using the chosen algorithm.
            - update model (TODO).

        Check and encode dataset to be used by the desired algorithm.

        Raises:
            ValueError if the dataset can't be used with the algorithm.

        """

        if not any(isinstance(dataset, i) for i in self._COMPATIBLE_DATASETS):
            msg = 'Dataset type (' + str(dataset.__class__.__name__)+ ') not suported by DMVLP model.'
            raise ValueError(msg)

        # TODO: add time serie management
        #eprint("algorithm set to " + str(self.algorithm))

        if self.algorithm == GULA:
            if not isinstance(dataset, StateTransitionsDataset):
                msg = 'Dataset type (' + str(dataset.__class__.__name__) + ') not supported \
                by the algorithm (' + str(self.algorithm.__class__.__name__) + '). \
                Dataset must be of type ' + str(StateTransitionsDataset.__class__.__name__)
                raise ValueError(msg)

            eprint("Starting fit with GULA")
            self.rules = GULA.fit(dataset=dataset) #, targets_to_learn={'y1': ['1']})

        # TODO
        #raise NotImplementedError('Not implemented yet')

    def predict(self, feature_state, semantics="synchronous"):
        """
        Predict the possible target states of the given feature state according to the model rules.

        Args:
            feature_state: list of String
                Feature state from wich target state must be predicted.
            semantics: String (optional)
                The dynamic semantics used to generate the target states.
        """
        feature_state_encoded = []
        for var_id, val in enumerate(feature_state):
            val_id = self.features[var_id][1].index(str(val))
            feature_state_encoded.append(val_id)

        #eprint(feature_state_encoded)

        target_states = []
        if semantics == "synchronous":
            target_states = Synchronous.next_new(feature_state_encoded, self.targets, self.rules)
        if semantics == "asynchronous":
            if len(self.features) != len(self.targets):
                raise ValueError("Asynchronous semantics can only be used if features and targets variables are the same.")
            target_states = Asynchronous.next_new(feature_state_encoded, self.targets, self.rules)

        return target_states

    def summary(self, line_length=None, print_fn=None):
        """
        Prints a string summary of the model.

        Args:
            line_length: int
                Total length of printed lines (e.g. set this to adapt the display to different terminal window sizes).
            print_fn: function
                Print function to use. Defaults to print.
                You can set it to a custom function in order to capture the string summary.
        """
        if self.algorithm is None:
            raise ValueError('Model has not been built: compile(algorithm) must be called before using summary.')

        # TODO: proper log, check Keras style

        if print_fn == None:
            print_fn = print
        print_fn(str(self.__class__.__name__) + " summary:")
        print_fn(" Algorithm: " + str(self.algorithm.__name__) + ' (' + str(self.algorithm) + ')')
        print_fn(" Features: ")
        for var in self.features:
            print_fn('  ' + str(var[0]) + ': ' + str(list(var[1])))
        print_fn(" Targets: ")
        for var in self.targets:
            print_fn('  ' + str(var[0]) + ': ' + str(list(var[1])))
        if len(self.rules) == 0:
            print_fn(' Rules: []')
        else:
            print_fn(" Rules:")
            for r in self.rules:
                print_fn("  "+r.logic_form(self.features, self.targets))

    def to_string(self):
        """
        Convert the object to a readable string

        Returns:
            String
                a readable representation of the object
        """
        output = " {"
        output += "Algorithm: " + str(self.algorithm.__name__)
        output += "\nFeatures: " + str(self.features)
        output += "\nTargets: " + str(self.targets)
        output += "\nRules:\n"
        for r in self.rules:
            output += r.logic_form(self.features, self.targets) + "\n"
        output += "}"

        return output

    def logic_form(self):
        """
        Convert the logic program to a logic programming string format

        Returns:
            String
                a logic programming representation of the logic program
        """
        output = ""

        # Variables declaration
        for var in range(len(self.features)):
            output += "FEATURE "+str(self.features[var][0])
            for val in self.features[var][1]:
                output += " " + str(val)
            output += "\n"

        for var in range(len(self.targets)):
            output += "TARGET "+str(self.targets[var][0])
            for val in self.targets[var][1]:
                output += " " + str(val)
            output += "\n"

        output += "\n"

        for r in self.rules:
            output += r.logic_form(self.features, self.targets) + "\n"

        return output

    def rules_of(self, var, val):
        """
        Specific head rule accessor method

        Args:
            var: int
                variable id
            val: int
                value id

        Returns:
            list of Rule
                rules of the program wich head is var=val
        """
        output = []
        for r in self.rules:
            if r.get_head_variable() == var and r.get_head_value() == val:
                output.append(r.copy())
        return output

#--------
# Static
#--------


#--------------
# Accessors
#--------------


    # TODO: check param type/format

    @property
    def features(self):
        return self._features

    @features.setter
    def features(self, value):
        if not isinstance(value, list):
            raise TypeError("features must be a list")
        if not all(isinstance(i, tuple) for i in value):
            raise TypeError("features must contain tuples")
        if not all(len(i)==2 for i in value):
            raise TypeError("features tuples must be of size 2")
        if not all(isinstance(domain, list) for (var,domain) in value):
            raise TypeError("features domains must be a list")
        if not all(isinstance(val, str) for (var,domain) in value for val in domain):
            raise ValueError("features domain values must be String")

        self._features = value.copy()

    @property
    def targets(self):
        return self._targets

    @targets.setter
    def targets(self, value):
        if not isinstance(value, list):
            raise TypeError("features must be a list")
        if not all(isinstance(i, tuple) for i in value):
            raise TypeError("features must contain tuples")
        if not all(len(i)==2 for i in value):
            raise TypeError("features tuples must be of size 2")
        if not all(isinstance(domain, list) for (var,domain) in value):
            raise TypeError("features domains must be a list")
        if not all(isinstance(val, str) for (var,domain) in value for val in domain):
            raise ValueError("features domain values must be String")

        self._targets = value.copy()

    @property
    def rules(self):
        return self._rules

    @rules.setter
    def rules(self, value):
        self._rules = value.copy()

    @property
    def algorithm(self):
        return self._algorithm

    @algorithm.setter
    def algorithm(self, value):
        self._algorithm = value
