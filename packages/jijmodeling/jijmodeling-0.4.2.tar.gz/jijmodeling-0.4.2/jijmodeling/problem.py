import copy
from jijmodeling.expression.expression import Add, Expression
from jijmodeling.extracte_vars import extracte_variables
from jijmodeling.expression.constraint import Constraint
from jijmodeling.transpilers.decode_from_sampleset import decode_variable
from jijmodeling.transpilers.shape_check import variables_validation
from jijmodeling.expression.utils import has_class
from jijmodeling.transpilers.calc_value import calc_value
from typing import Optional, List, Dict, Tuple
import dimod


class Problem():
    """represents optimization problem

    Attributes:
        placeholders (dict)
    """
    def __init__(self, problem_name: str) -> None:
        self.obj_vars = {}
        self.placeholders = {}
        self.name = problem_name
        self.model: Optional[Expression] = None
        self.cost = 0
        self.constraints: Dict[str, Expression] = {}

        self._placeholder = None
        self._fixed_variables = None

    def __repr__(self) -> str:
        return '{}: {}'.format(self.name, self.model)

    def __add__(self, other):
        """add mathematical model component (cost and constraints)

        Args:
            other (:class:`Expression`): mathematical model component

        Returns:
            Problem: self
        """
        if self.model is None:
            self.model = other
        else:
            self.model += other

        cost, consts = divide_constraints(other)
        self.cost = cost if self.cost == 0 else self.cost + cost
        self.constraints.update(consts)
        return self

    def to_pyqubo(self, placeholder: dict = {}, fixed_variables: dict = {}):
        variables = extracte_variables(self.model)
        variables_validation(placeholder, variables)
        self._placeholder = placeholder
        self._fixed_variables = fixed_variables
        return self.model.to_pyqubo(
                placeholder=placeholder,
                fixed_variables=fixed_variables,
                )

    def decode(
            self,
            response: dimod.SampleSet,
            placeholder: dict = None,
            fixed_variables: dict = None,
            calc_value: bool = True) -> List[Dict[str, dict]]:
        """decode dimod.SampleSet object.

        Validation check for constraint conditions and decode
        by meta info of each term classes.

        Args:
            response (dimod.SampleSet): response
            from dimod.Sampler or openjij's sampler

        Returns:
            List[Dict[str, dict]]: {'solution': decoded solution (dict),
            'penalty': value of each penalty (dict),
            'cost': cost value without penalty term (float).}
        """

        if self._placeholder is None and self._fixed_variables is None:
            if placeholder is None:
                raise TypeError(
                    "decode() missing 1 required argument: 'placeholder'")
            if fixed_variables is None:
                raise TypeError(
                    "decode() missing 1 required argument: 'fixed_variables'")
            self._placeholder = placeholder
            self._fixed_variables = fixed_variables

        decoded = []
        variables = extracte_variables(self.model)
        # decode variables
        for sample in response.samples():
            vars_value = {}
            for var in variables['obj_vars'].values():
                vars_value.update(decode_variable(
                                    var,
                                    sample=dict(sample),
                                    placeholder=self._placeholder,
                                    fixed_variables=self._fixed_variables))

            # replace fixed variables
            for label, fixed_val in self._fixed_variables.items():
                if isinstance(fixed_val, dict):
                    for key, value in fixed_val.items():
                        vars_value[label][key] = value
                else:
                    # scalar case
                    vars_value[label] = fixed_val

            if calc_value:
                # calculate constraint penalies
                penalty = self.calc_penalty(vars_value)
                # calculate cost (with out penalty term)
                cost = self.calc_cost(vars_value)
            else:
                penalty, cost = None, None

            decoded.append(
                {
                    'solution': vars_value,
                    'penalty': penalty,
                    'cost': cost
                 }
            )

        return decoded

    def calc_penalty(self, solution):
        penalties = {}
        for k, const in self.constraints.items():
            mul_const = {k: 1.0}
            ph_value = copy.copy(self._placeholder)
            ph_value.update(mul_const)
            penalties[k] = const.calc_value(
                decoded_sol=solution,
                placeholder=ph_value,
                fixed_indices={}
            )
        return penalties

    def calc_cost(self, solution):
        return calc_value(
            self.cost,
            decoded_sol=solution,
            placeholder=self._placeholder,
            fixed_indices={}
        )

    # def to_pulp(self, placeholder: dict={}, fixed_variables: dict={}, sense: int=1):
    #     self._placeholder = placeholder
    #     self._fixed_variables = fixed_variables
    #     objective, constraints, vars = to_pulp(self.model, placeholder=placeholder, fixed_variables=fixed_variables)

    #     import pulp
    #     problem = pulp.LpProblem(sense=sense)
    #     problem += objective
    #     for cons in constraints:
    #         problem += cons
    #     return problem, vars


    # def _repr_latex_(self):
    #     opt_model = r"$$\begin{align}"
    #     opt_model += r"\min~&" + (self.cost.__latex__() if isinstance(self.cost, Expression) else str(self.cost))
    #     def condition_str(cond):
    #         if cond == '==': return '='
    #         elif cond == '<=': return r'\leq'
    #         elif cond == '<': return '<'
    #         else: return cond

    #     if len(self.constraints) > 0:
    #         opt_model += r"\\ \mathrm{s.t.}~"
    #         for cons, term in self.constraints.items():
    #             opt_model += "&" + term.__latex__() +  condition_str(term.condition) + str(term.constant) + r"\\ "
    #         opt_model = opt_model[:-3] 
    #         opt_model += r"\end{align}$$"
    #     return opt_model


def divide_constraints(
        expression: Expression) -> Tuple[Expression, Dict[str, Expression]]:
    if isinstance(expression, Add):
        constraints = {}
        cost_term = 0
        for child in expression.children:
            cost, consts = divide_constraints(child)
            cost_term += cost
            constraints.update(consts)
        return cost_term, constraints

    if has_class(expression, Constraint):
        def get_label(constraint: Expression):
            if isinstance(constraint, Constraint):
                return constraint.label
            for child in constraint.children:
                label = get_label(child)
                if label is not None:
                    return label
            return None
        const_label = get_label(expression)
        return 0, {const_label: expression}

    return expression, {}
