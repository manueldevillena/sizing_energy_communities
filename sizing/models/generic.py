import os
import pandas as pd
import pyomo.environ as pyo

from abc import ABC

from sizing.core import OptimisationInputs
from sizing.utils import unstack_data

DEFAULT_FREQ = '15T'


class GenericModel(ABC):
    """
    Generic object with generic methods shared by all models.
    """

    def __init__(self, inputs: OptimisationInputs, solver: str = 'cbc'):
        """
        Constructor.
        :param inputs: inputs for the simulation.
        :param solver: solver to be used to solve the model.
        """
        self.inputs = inputs
        self.solver_name = solver
        self.annuity_factor = self._compute_annuity_factor(self.inputs.interest_rate, self.inputs.lifetime)
        self.discount_factor = self._compute_discount_factor(self.inputs.discount_rate, self.inputs.lifetime)
        self.frequency = self._infer_frequency(self.inputs.demand.index)

    def _post_process(self, model: pyo.ConcreteModel):
        """
        Extracts and processes the results of the optimisation.
        :param model: model containing the variables and equations to be solved.
        :return results of the optimisation.
        """
        results = dict()
        for variable_name in ['optimal_capacity', 'annual_investment_costs', 'annual_operational_costs',
                              'annual_electricity_bills', 'annual_electricity_revenue', 'total_costs',
                              'imports_retailer', 'imports_rec', 'exports_retailer', 'exports_rec',
                              'electricity_produced', 'electricity_consumed']:
            try:
                # Get the value of the variable with the same name
                data = getattr(model, variable_name).get_values()
            except AttributeError:
                raise AttributeError(
                    """The argument "variable" only accepts "optimized_keys", "allocated_consumption",
                    "verified_allocated_consumption", "locally_sold_production", "ssr_user" or "ssr_rec",
                    otherwise leave it empty."""
                )
            output_data = pd.Series(data)
            results[f'{variable_name}'] = unstack_data(output_data)

        duals = dict()
        for constraint in model.component_objects(pyo.Constraint, active=True):
            indices = [i for i in constraint]
            if isinstance(indices[0], tuple):
                index = pd.MultiIndex.from_tuples(indices)
                dual_values = pd.Series(index=index)
            else:
                dual_values = pd.Series(index=indices)
            for index in constraint:
                dual_values[index] = model.dual[constraint[index]]
            duals[f'dual{constraint.name}'] = unstack_data(dual_values)

        self._save_results(inputs=self.inputs, results=results)
        self._save_results(inputs=self.inputs, results=duals)

        return results, duals

    def solve_model(self, model: pyo.ConcreteModel):
        """
        Solves the model previously created.
        :param model: model containing the variables and equations to be solved.
        :return results of the optimisation.
        """
        opt = pyo.SolverFactory(self.solver_name)
        results = opt.solve(model, tee=True, keepfiles=False)

        if (results.solver.status != pyo.SolverStatus.ok
                or results.solver.termination_condition not in {
                    pyo.TerminationCondition.optimal,
                    pyo.TerminationCondition.feasible
                }
        ):
            raise ValueError(f"""Problem not properly solved (status: {results.solver.status}, 
                termination condition: {results.solver.termination_condition}).""")

        return self._post_process(model)

    def create_model(self, inputs: OptimisationInputs):
        """
        Optimisation model.
        :param inputs: input data and parameters.
        :return: model
        """
        raise NotImplementedError

    @staticmethod
    def _save_results(inputs: OptimisationInputs, results: dict):
        """
        Saves the results in csv files.
        :param inputs: input data and parameters.
        :param results: dictionary containing the results of the simulation..
        """
        for key, values in results.items():
            values.to_csv(os.path.join(inputs.output_path, f'{key}.csv'))

    @staticmethod
    def _compute_annuity_factor(interest_rate: float, lifetime: int) -> float:
        """
        Computes the annuity factor as a function of the interest rate and the lifetime of the REC.
        :param interest_rate: scalar representing the average interest rate of the REC.
        :param lifetime: integer representing the lifetime of the REC in years.
        :return: annuity factor.
        """
        try:
            annuity_factor = interest_rate / (1 - (1 + interest_rate)**(-lifetime))
        except ZeroDivisionError:
            annuity_factor = 1 / lifetime

        return annuity_factor

    @staticmethod
    def _compute_discount_factor(discount_rate: float, lifetime: int) -> float:
        """
        Computes the discount factor to be applied to the annual costs as a function of the discount rate and the lifetime of the REC.
        :param discount_rate: scalar representing the discount rate.
        :param lifetime: integer representing the lifetime of the REC in years.
        :return: discount factor.
        """
        try:
            discount_factor = (1 - (1 + discount_rate)**(-lifetime - 1)) / (1 - (1 + discount_rate)**(-1))
        except ZeroDivisionError:
            discount_factor = 1

        return discount_factor

    @staticmethod
    def _infer_frequency(timeseries: pd.timedelta_range) -> int:
        """
        Finds the resolution of a time series.
        :param timeseries: time index of the optimisation problem.
        :return: resolution (frequency) of the time index.
        """
        try:
            freq = pd.infer_freq(timeseries)
        except ValueError:
            freq = DEFAULT_FREQ

        if freq == '15T':
            return int(15)
        elif freq == 'H':
            return int(60)
