#-----------------------
# @author: Tony Ribeiro
# @created: 2019/10/29
# @updated: 2019/10/29
#
# @desc: simple implementation synchronous semantic over LogicProgram
#   - Update all variables at the same time
#   - Can generate non-deterministic transitions
#-----------------------

#from semantics import Semantics
#from utils import eprint
#from rule import Rule
#from logicProgram import LogicProgram
from .. import utils
from ..objects import rule
from ..objects import logicProgram
from ..semantics.semantics import Semantics
from ..utils import eprint

import itertools

class Synchronous(Semantics):
    """
    Define the synchronous semantic over discrete multi-valued logic program
    """
    @staticmethod
    def next_new(state, targets, rules):
        """
        Compute the next state according to the rules and the synchronous semantics.

        Args:
            state: list of String.
                A state of the system.
            targets: list of String.
                List of target variables.
                Order must correspond to rules encoding.
                The target states will have same order of variables.
            rules: list of Rules.
                A list of multi-valued logic rules.

        Returns:
            list of (list of int).
                the possible next states according to the rules.
        """
        #eprint("-- Args --")
        #eprint("state: ", state)
        #eprint("targets: ", targets)
        #eprint("rules: ", rules)

        output = []
        domains = [set() for var in targets]

        # extract conclusion of all matching rules
        for r in rules:
            if(r.matches(state)):
                domains[r.get_head_variable()].add(r.get_head_value())

        # DBG
        #eprint("domains: ", domains)

        # Check variables without next value
        for i,domain in enumerate(domains):
            if len(domain) == 0:
                domains[i] = [-1]

        # generate all combination of domains
        possible = set([i for i in list(itertools.product(*domains))])

        # DBG
        #eprint("possible: ", possible)

        # Decode target states
        output = []
        for s in possible:
            target_state = []
            for var_id, val_id in enumerate(s):
                #eprint(var_id, val_id)
                if val_id == -1:
                    target_state.append("?")
                else:
                    target_state.append(targets[var_id][1][val_id])
            output.append(target_state)

        #eprint(output)

        return output


    @staticmethod
    def next(program, state, default=None):
        """
        Compute the next state according to the rules of the program.

        Args:
            program: LogicProgram
                A multi-valued logic program
            state: list of string
                A state of the system
            default: list of list of int
                Optional default values for each variable if no rule match
                If not given state value will be considered

        Returns:
            list of (list of int)
                the possible next states according to the rules of the program.
        """
        # Check arguments
        if default != None:
            if len(default) != len(program.get_targets()) or [] in default:
                raise ValueError("default must be None or must give a list of values for each target variable")

        # Convert state to feature value ids
        encoded_state = [str(i) for i in state]
        for var, val in enumerate(encoded_state):
            val_id = program.get_features()[var][1].index(val)
            encoded_state[var] = val_id
        state = encoded_state

        output = []
        domains = [set() for var in program.get_targets()]

        # extract conclusion of all matching rules
        for r in program.get_rules():
            if(r.matches(state)):
                domains[r.get_head_variable()].add(r.get_head_value())

        # Check variables without next value
        for i,domain in enumerate(domains):
            if len(domain) == 0:
                if default == None:
                    domains[i] = set([0]) # TODO: add option for projection
                    #if i < len(state):
                    #    domains[i] = set([state[i]])
                else:
                    domains[i] = set(default[i])

        # generate all combination of conclusions
        possible = set([i for i in list(itertools.product(*domains))])

        # DBG
        #eprint("state: ", state)
        #eprint("possible: ", possible)

        # apply constraints
        output = []
        for s in possible:
            valid = True
            for c in program.get_constraints():
                if c.matches(list(state)+list(s)):
                    valid = False
                    break
            if valid:
                # Decode state with domain values
                output.append([ program.get_targets()[var][1][val] for var,val in enumerate(s) ])

        # DBG
        #eprint("constrainted: ", output)

        return output

    @staticmethod
    def transitions(program, default=None):
        output = []
        for s1 in program.feature_states():
            next_states = Synchronous.next(program, s1, default)
            for s2 in next_states:
                output.append([list(s1),list(s2)])
        return output
