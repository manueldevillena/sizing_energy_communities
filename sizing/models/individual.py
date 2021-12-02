import pandas as pd
import pyomo.environ as pyo

from sizing.core import OptimisationInputs
from . import GenericModel


class Individual(GenericModel):
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
            return self.inputs.initial_capacity.loc[u, n], self.inputs.maximum_capacity

        # Linear program
        m = pyo.ConcreteModel()

        # Extraction dual variables
        m.dual = pyo.Suffix(direction=pyo.Suffix.IMPORT)

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

        ####################
        # Objective function
        ####################

        def _objective_function(m):
            """
            Minimises the sum of costs (investment, operation, electricity) taking away the revenue.
            """
            return pyo.quicksum(m.total_costs[u] for u in m.member) * self.discount_factor

        #############
        # Constraints
        #############
        def _total_costs(m, u):
            """
            Computes the total costs per REC member.
            """
            return m.total_costs[u] == (
                    m.annual_investment_costs[u] +
                    m.annual_operational_costs[u] +
                    m.annual_electricity_bills[u] -
                    m.annual_electricity_revenue[u]
            )

        def _annual_investments(m, u):
            """
            Annuity of the initial investments over the lifetime of the REC.
            """
            return m.annual_investment_costs[u] == (
                pyo.quicksum(
                    (m.optimal_capacity[u, n] - self.inputs.initial_capacity.loc[u, n]) *
                    self.inputs.cost_technology_investment.loc[u, n] * self.annuity_factor
                    for n in m.technology
                )
            )

        def _annual_operational_costs(m, u):
            """
            Annual operational costs.
            """
            return m.annual_operational_costs[u] == (
                pyo.quicksum(
                    self.inputs.cost_technology_running_fixed.loc[u, n] * m.optimal_capacity[u, n] +
                    pyo.quicksum(
                        self.inputs.cost_technology_running_variable * (m.electricity_produced[t, u] + m.electricity_consumed[t, u])
                        for t in m.time
                    )
                    for n in m.technology
                )
            )

        def _annual_electricity_bills(m, u):
            """
            Annual electricity bills.
            """
            return m.annual_electricity_bills[u] == (
                pyo.quicksum(
                    m.imports_retailer[t, u] * self.inputs.prices_grid_import.loc[t, u] +
                    m.imports_rec[t, u] * self.inputs.prices_community_import.loc[t, u] +
                    m.imports_rec[t, u] * self.inputs.prices_community_exchange.loc[t][0]
                    for t in m.time
                )
            )

        def _annual_electricity_revenue(m, u):
            """
            Annual electricity revenue.
            """
            return m.annual_electricity_revenue[u] == (
                pyo.quicksum(
                    m.exports_retailer[t, u] * self.inputs.prices_grid_export.loc[t, u] +
                    m.exports_rec[t, u] * self.inputs.prices_community_exchange.loc[t][0]
                    for t in m.time
                )
            )

        def _technology_generation(m, t, u):
            """
            Power generated by the different technologies.
            """
            return m.electricity_produced[t, u] == (
                    self.inputs.generation.loc[t, u] * m.optimal_capacity[u, 'p'] + m.battery_outflow[t, u]
            )

        def _technology_consumption(m, t, u):
            """
            Power consumed by the different technologies.
            """
            return m.electricity_consumed[t, u] == m.battery_inflow[t, u]

        def _state_of_charge(m, t, u):
            """
            Computes the state of charge of the battery.
            """
            if t == m.time[1]:
                return m.battery_soc[t, u] == m.battery_soc[m.time[-1], u]
            else:
                return m.battery_soc[t, u] == (
                    m.battery_soc[t-pd.Timedelta(minutes=self.frequency), u] +
                    self.inputs.efficiency_charge * m.battery_inflow[t, u] -
                    m.battery_outflow[t, u] / self.inputs.efficiency_discharge
                )

        def _state_of_charge_limit(m, t, u):
            """
            Limits the maximum state of charge to the capacity of the battery.
            """
            return m.battery_soc[t, u] <= m.optimal_capacity[u, 'b']

        def _limit_inflow(m, t, u):
            """
            Limits the battery inflow.
            """
            return m.battery_inflow[t, u] <= m.optimal_capacity[u, 'b'] / self.inputs.charge_rate

        def _limit_outflow(m, t, u):
            """
            Limits the battery inflow.
            """
            return m.battery_outflow[t, u] <= m.optimal_capacity[u, 'b'] / self.inputs.discharge_rate

        def _energy_balance(m, t, u):
            """
            Energy balance of the REC.
            """
            return (
                self.inputs.demand.loc[t, u] +
                m.exports_retailer[t, u] +
                m.exports_rec[t, u] +
                m.electricity_consumed[t, u]
                ==
                m.electricity_produced[t, u] +
                m.imports_retailer[t, u] +
                m.imports_rec[t, u]
            )

        def _limit_exports(m, t, u):
            """
            Limits the total exports to the electricity produced.
            """
            return m.exports_rec[t, u] + m.exports_retailer[t, u] <= m.electricity_produced[t, u]

        ###################
        # Calling equations
        ###################

        m.objective_eqn = pyo.Objective(rule=_objective_function, sense=pyo.minimize)
        m._total_costs_eqn = pyo.Constraint(m.member, rule=_total_costs)
        m._annual_investments_eqn = pyo.Constraint(m.member, rule=_annual_investments)
        m._annual_operational_costs_eqn = pyo.Constraint(m.member, rule=_annual_operational_costs)
        m._annual_electricity_bills_eqn = pyo.Constraint(m.member, rule=_annual_electricity_bills)
        m._annual_electricity_revenue_eqn = pyo.Constraint(m.member, rule=_annual_electricity_revenue)
        m._technology_generation_eqn = pyo.Constraint(m.time, m.member, rule=_technology_generation)
        m._technology_consumption_eqn = pyo.Constraint(m.time, m.member, rule=_technology_consumption)
        m._state_of_charge_eqn = pyo.Constraint(m.time, m.member, rule=_state_of_charge)
        m._state_of_charge_limit_eqn = pyo.Constraint(m.time, m.member, rule=_state_of_charge_limit)
        m._limit_inflow_eqn = pyo.Constraint(m.time, m.member, rule=_limit_inflow)
        m._limit_outflow_eqn = pyo.Constraint(m.time, m.member, rule=_limit_outflow)
        m._energy_balance_eqn = pyo.Constraint(m.time, m.member, rule=_energy_balance)
        m._limit_exports_eqn = pyo.Constraint(m.time, m.member, rule=_limit_exports)

        if self._is_debug:
            m.write(f'{self.inputs.output_path}/model.lp', io_options={'symbolic_solver_labels': True})

        return m
