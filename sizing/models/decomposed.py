import pyomo.environ as pyo

import sizing.constraints.constraints as cs
from sizing.core import OptimisationInputs
from sizing.technologies import SolarPanel
from . import GenericModel


class Decomposed(GenericModel):
    """
    Planing problem from a fully centralised optimisation standpoint.
    """

    def __init__(self, inputs: OptimisationInputs, solver: str = 'cbc', is_debug: bool = False):
        """
        Constructor.
        :param inputs: input data and parameters.
        :param solver: name of the solver to use.
        :param is_debug: flag to activate debug mode.
        """
        super().__init__(inputs, solver)
        self._is_debug = is_debug

    def create_model(self, **kwargs):
        """
        Optimisation model.
        :return: model
        """
        def _initialise_optimal_capacity(m, u, n):
            """
            Defines the initial optimal capacity of the REC members.
            """
            return self.inputs.initial_capacity.loc[u, n], 1000

        # Linear program
        m = pyo.ConcreteModel()

        # Sets
        m.time = pyo.Set(initialize=self.inputs.demand.index)
        m.member = pyo.Set(initialize=self.inputs.demand.columns)
        m.technology = pyo.Set(initialize=['p', 'b'])

        # Decision variables
        m.optimal_capacity = pyo.Var(m.member, m.technology, bounds=_initialise_optimal_capacity)
        m.electricity_produced = pyo.Var(m.time, m.member, within=pyo.NonNegativeReals)
        m.electricity_consumed = pyo.Var(m.time, m.member, within=pyo.NonNegativeReals)
        m.imports_retailer = pyo.Var(m.time, m.member, within=pyo.NonNegativeReals)
        m.imports_rec = pyo.Var(m.time, m.member, within=pyo.NonNegativeReals)
        m.exports_retailer = pyo.Var(m.time, m.member, within=pyo.NonNegativeReals)
        m.exports_rec = pyo.Var(m.time, m.member, within=pyo.NonNegativeReals)
        m.battery_outflow = pyo.Var(m.time, m.member, within=pyo.NonNegativeReals)
        m.battery_inflow = pyo.Var(m.time, m.member, within=pyo.NonNegativeReals)
        m.battery_soc = pyo.Var(m.time, m.member, within=pyo.NonNegativeReals)

        # Auxiliary variables
        m.annual_investment_costs = pyo.Var(m.member, within=pyo.NonNegativeReals)
        m.annual_operational_costs = pyo.Var(m.member, within=pyo.NonNegativeReals)
        m.annual_electricity_bills = pyo.Var(m.member, within=pyo.NonNegativeReals)
        m.annual_electricity_revenue = pyo.Var(m.member, within=pyo.NonNegativeReals)
        m.total_costs = pyo.Var(m.member, within=pyo.NonNegativeReals)

        return m

    def call_equations(self, m):
        """
        Calling equations.
        """
        m.objective_eqn = pyo.Objective(rule=cs.objective_function, sense=pyo.minimize)
        m._total_costs_eqn = pyo.Constraint(m.member, rule=cs.total_costs)
        m._annual_investments_eqn = pyo.Constraint(m.member, rule=cs.annual_investments)
        m._annual_operational_costs_eqn = pyo.Constraint(m.member, rule=cs.annual_operational_costs)
        m._annual_electricity_bills_eqn = pyo.Constraint(m.member, rule=cs.annual_electricity_bills)
        m._annual_electricity_revenue_eqn = pyo.Constraint(m.member, rule=cs.annual_electricity_revenue)
        m._technology_consumption_eqn = pyo.Constraint(m.time, m.member, rule=cs.technology_consumption)
        m._state_of_charge_eqn = pyo.Constraint(m.time, m.member, rule=cs.state_of_charge)
        m._state_of_charge_limit_eqn = pyo.Constraint(m.time, m.member, rule=cs.state_of_charge_limit)
        m._limit_inflow_eqn = pyo.Constraint(m.time, m.member, rule=cs.limit_inflow)
        m._limit_outflow_eqn = pyo.Constraint(m.time, m.member, rule=cs.limit_outflow)
        m._energy_balance_eqn = pyo.Constraint(m.time, m.member, rule=cs.energy_balance)
        m._local_exchanges_eqn = pyo.Constraint(m.time, rule=cs.local_exchanges)

        self.PV = SolarPanel(self.inputs, m)
        self.PV.pv_generation()
