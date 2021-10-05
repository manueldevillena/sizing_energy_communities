import pandas as pd
import pyomo.environ as pyo

from sizing.core import OptimisationInputs
from . import GenericModel


class Central(GenericModel):
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
        super().__init__(solver)
        self._inputs = inputs
        self._is_debug = is_debug

    def _post_process(self, model: pyo.ConcreteModel):
        """
        Extracts and processes the results of the optimisation.
        :param model: model containing the variables and equations to be solved.
        :return results of the optimisation.
        """
        output = dict()
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
            if type(output_data.index) == pd.core.indexes.multi.MultiIndex:
                output_data = output_data.unstack()

            output[f'{variable_name}'] = output_data

        self._save_results(inputs=self._inputs, results=output)
        return output

    def create_model(self, **kwargs):
        """
        Optimisation model.
        :return: model
        """
        # Pre-processing
        annuity_factor, discount_rate, frequency = self._pre_process()

        def _initialise_optimal_capacity(m, u, n):
            """
            Defines the initial optimal capacity of the REC members.
            """
            return self._inputs.initial_capacity.loc[u, n], 1000

        # Linear program
        m = pyo.ConcreteModel()

        # Sets
        m.time = pyo.Set(initialize=self._inputs.demand_members.index)
        m.member = pyo.Set(initialize=self._inputs.demand_members.columns)
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
            return pyo.quicksum(m.total_costs[u] for u in m.member) * discount_rate

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
                    (m.optimal_capacity[u, n] - self._inputs.initial_capacity.loc[u, n]) *
                    self._inputs.cost_technology.loc[u, n] * annuity_factor
                    for n in m.technology
                )
            )

        def _annual_operational_costs(m, u):
            """
            Annual operational costs.
            """
            return m.annual_operational_costs[u] == (
                pyo.quicksum(
                    self._inputs.cost_technology_running_fixed.loc[u, n] * m.optimal_capacity[u, n] +
                    pyo.quicksum(
                        self._inputs.cost_technology_running_variable * (m.electricity_produced[t, u] + m.electricity_consumed[t, u])
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
                    m.imports_retailer[t, u] * self._inputs.prices_import_grid_members.loc[t, u] +
                    m.imports_rec[t, u] * self._inputs.prices_import_local_members.loc[t, u]
                    for t in m.time
                )
            )

        def _annual_electricity_revenue(m, u):
            """
            Annual electricity revenue.
            """
            return m.annual_electricity_revenue[u] == (
                pyo.quicksum(
                    m.exports_retailer[t, u] * self._inputs.prices_export_grid_members.loc[t, u] +
                    m.exports_rec[t, u] * self._inputs.prices_export_local_members.loc[t, u]
                    for t in m.time
                )
            )

        def _technology_generation(m, t, u):
            """
            Power generated by the different technologies.
            """
            return m.electricity_produced[t, u] == (
                    self._inputs.production_members.loc[t, u] * m.optimal_capacity[u, 'p'] + m.battery_outflow[t, u]
            )

        def _technology_consumption(m, t, u):
            """
            Power consumed by the different technologies.
            """
            return m.electricity_consumed[t, u] >= m.battery_inflow[t, u]

        def _state_of_charge(m, t, u):
            """
            Computes the state of charge of the battery.
            """
            if t == m.time[1]: # TODO: Are we sure this should not be m.time[0]?
                return m.battery_soc[t, u] == m.battery_soc[m.time[-1], u]
            else:
                return m.battery_soc[t, u] == (
                    m.battery_soc[t-pd.Timedelta(minutes=frequency), u] +
                    self._inputs.efficiency_charge * m.battery_inflow[t, u] -
                    m.battery_outflow[t, u] / self._inputs.efficiency_discharge
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
            return m.battery_inflow[t, u] <= m.optimal_capacity[u, 'b'] / self._inputs.charge_rate

        def _limit_outflow(m, t, u):
            """
            Limits the battery inflow.
            """
            return m.battery_outflow[t, u] <= m.optimal_capacity[u, 'b'] / self._inputs.discharge_rate

        def _energy_balance(m, t, u):
            """
            Energy balance of the REC.
            """
            return (
                self._inputs.demand_members.loc[t, u] +
                m.exports_retailer[t, u] +
                m.exports_rec[t, u] +
                m.electricity_consumed[t, u]
                ==
                m.electricity_produced[t, u] +
                m.imports_retailer[t, u] +
                m.imports_rec[t, u]
            )

        def _local_exchanges(m, t):
            """
            Ensures that exports to the REC are equal to imports from the REC.
            """
            return (
                pyo.quicksum(m.exports_rec[t, u] for u in m.member)
                ==
                pyo.quicksum(m.imports_rec[t, u] for u in m.member)
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
        m._local_exchanges_eqn = pyo.Constraint(m.time, rule=_local_exchanges)
        # m._limit_exports_eqn = pyo.Constraint(m.time, m.member, rule=_limit_exports)

        if self._is_debug:
            m.write('{}/model.lp'.format(self._inputs.output_path), io_options={'symbolic_solver_labels': True})

        return m

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
