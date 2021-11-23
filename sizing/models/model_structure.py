import pyomo.environ as pyo

from sizing.core import OptimisationInputs


BOUND_TECH = 1000


class ModelStructure:
    """
    Creates the model.
    """

    def __init__(self, inputs: OptimisationInputs):
        """
        Constructor.
        """
        self.inputs = inputs

    def initialise_problem(self, model):
        """
        Initialises the sets and variables of a pyomo model (parameters are not initialised as pyomo but as python objects).

        :param model: Pyomo model where sets and variables are initialised.
        """
        def _initialise_optimal_capacity(model, m, n):
            """
            Defines the initial optimal capacity of the REC members.

            :param model: Pyomo model.
            :param m: Member m.
            :param n: Technology n.
            """
            return self.inputs.initial_capacity.loc[u, n], BOUND_TECH

        # Sets initialisation
        model.time = pyo.Set(initialize=self.inputs.demand.index)
        model.member = pyo.Set(initialize=self.inputs.demand.columns)
        model.technology = pyo.Set(initialize=['p', 'b'])

        # Decision variables initialisation
        model.optimal_capacity = pyo.Var(model.member, model.technology, bounds=_initialise_optimal_capacity)
        model.electricity_produced = pyo.Var(model.time, model.member, within=pyo.NonNegativeReals)
        model.electricity_consumed = pyo.Var(model.time, model.member, within=pyo.NonNegativeReals)
        model.imports_retailer = pyo.Var(model.time, model.member, within=pyo.NonNegativeReals)
        model.imports_rec = pyo.Var(model.time, model.member, within=pyo.NonNegativeReals)
        model.exports_retailer = pyo.Var(model.time, model.member, within=pyo.NonNegativeReals)
        model.exports_rec = pyo.Var(model.time, model.member, within=pyo.NonNegativeReals)
        model.battery_outflow = pyo.Var(model.time, model.member, within=pyo.NonNegativeReals)
        model.battery_inflow = pyo.Var(model.time, model.member, within=pyo.NonNegativeReals)
        model.battery_soc = pyo.Var(model.time, model.member, within=pyo.NonNegativeReals)

        # Auxiliary variables initialisation
        model.annual_investment_costs = pyo.Var(model.member, within=pyo.NonNegativeReals)
        model.annual_operational_costs = pyo.Var(model.member, within=pyo.NonNegativeReals)
        model.annual_electricity_bills = pyo.Var(model.member, within=pyo.NonNegativeReals)
        model.annual_electricity_revenue = pyo.Var(model.member, within=pyo.NonNegativeReals)
        model.total_costs = pyo.Var(model.member, within=pyo.NonNegativeReals)
