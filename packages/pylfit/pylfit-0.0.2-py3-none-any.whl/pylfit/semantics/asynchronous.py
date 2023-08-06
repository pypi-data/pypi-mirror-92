#-----------------------
# @author: Tony Ribeiro
# @created: 2020/07/14
# @updated: 2020/07/14
#
# @desc: simple implementation of asynchronous semantic over LogicProgram
#   - Update atmost one variables at a time
#   - Can generate non-deterministic transitions
#-----------------------

from ..utils import eprint
from ..objects.rule import Rule
from ..objects.logicProgram import LogicProgram
from ..semantics.semantics import Semantics

import itertools

class Asynchronous(Semantics):
    """
    Define the asynchronous semantic over discrete multi-valued logic program
    Assume feature=targets
    """

    @staticmethod
    def next_new(state, targets, rules):
        """
        Compute the next state according to the rules and the asynchronous semantics.

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

        # TODO: add projection to argument to handle different features/targets

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
        possible = []

        # next is state with one replacement
        for var_id in range(0,len(domains)):
            for val in domains[var_id]:
                if state[var_id] != val:
                    s2 = list(state)
                    s2[var_id] = val
                    possible.append(s2)

        # Self loop if no possible transitions
        if len(possible) == 0:
            possible.append(state)

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
            state: list of int
                A state of the system
            default: list of list of int
                Optional default values for each variable if no rule match
                If not given state value will be considered

        Returns:
            list of (list of int)
                the possible next states according to the rules of the program.
        """

        output = []
        domains = [set() for var in program.get_targets()]

        # extract conclusion of all matching rules
        for r in program.get_rules():
            if(r.matches(state)):
                domains[r.get_head_variable()].add(r.get_head_value())

        # Add default for variables without matching rules
        if default != None:
            if len(default) != len(program.get_targets()):
                raise ValueError("default must be None or must give a list of value (empty included) for each target variable")

            for var in range(0,len(program.get_targets())):
                if len(domains[var]) == 0:
                    domains[var] = set(default[var])

        # next is state with one replacement
        for var in range(0,len(domains)):
            for val in domains[var]:
                if state[var] != val:
                    s2 = list(state)
                    s2[var] = val
                    output.append(tuple(s2))

        # Self loop if no possible transitions
        if len(output) == 0:
            output.append(state)

        output = set(output)

        return output

    @staticmethod
    def transitions(program, default=None):
        output = []
        for s1 in program.states():
            next_states = Asynchronous.next(program, s1, default)
            for s2 in next_states:
                output.append([s1,s2])
        return output
