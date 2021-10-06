import pandas as pd
import pyomo.environ as pyo

from abc import ABC
from sizing.core import OptimisationInputs

DEFAULT_FREQ = '15T'


class GenericModel(ABC):
    """
    Generic object with generic methods shared by all models.
    """

    def __init__(self, solver: str = 'cbc'):
        """
        Constructor.
        :param solver: solver to be used to solve the model.
        """
        self.solver_name = solver

    def _pre_process(self):
        """
        Pre-processing specific to each model.
        :return: pre-processed data.
        """
        annuity_factor = self._compute_annuity_factor(self._inputs.interest_rate, self._inputs.lifetime)
        discount_factor = self._compute_discount_factor(self._inputs.discount_rate, self._inputs.lifetime)
        frequency = self._infer_frequency(self._inputs.demand.index)

        return annuity_factor, discount_factor, frequency

    def create_model(self, inputs: OptimisationInputs):
        """
        Optimisation model.
        :param inputs: input data and parameters.
        :return: model
        """
        raise NotImplementedError

    def solve_model(self, model: pyo.ConcreteModel):
        """
        Solves the model previously created.
        :param model: model containing the variables and equations to be solved.
        :return results of the optimisation.
        """
        raise NotImplementedError

    def _post_process(self, model: pyo.ConcreteModel):
        """
        Extracts and processes the results of the optimisation.
        :param model: model containing the variables and equations to be solved.
        :return results of the optimisation.
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
            values.to_csv('{output}{name}.csv'.format(name=key, output=inputs.output_path))

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
