import pyomo.environ as pyo


def objective_function(m):
    """
    Minimises the sum of costs (investment, operation, electricity) taking away the revenue.
    """
    return pyo.quicksum(m.total_costs[u] for u in m.member) * discount_rate


def total_costs(m, u):
    """
    Computes the total costs per REC member.
    """
    return m.total_costs[u] == (
            m.annual_investment_costs[u] +
            m.annual_operational_costs[u] +
            m.annual_electricity_bills[u] -
            m.annual_electricity_revenue[u]
    )


def annual_investments(m, u):
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


def annual_operational_costs(m, u):
    """
    Annual operational costs.
    """
    return m.annual_operational_costs[u] == (
        pyo.quicksum(
            self._inputs.cost_technology_running_fixed.loc[u, n] * m.optimal_capacity[u, n] +
            pyo.quicksum(
                self._inputs.cost_technology_running_variable *
                (m.electricity_produced[t, u] + m.electricity_consumed[t, u])
                for t in m.time
            )
            for n in m.technology
        )
    )


def annual_electricity_bills(m, u):
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


def annual_electricity_revenue(m, u):
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


def technology_consumption(m, t, u):
    """
    Power consumed by the different technologies.
    """
    return m.electricity_consumed[t, u] >= m.battery_inflow[t, u]


def state_of_charge(m, t, u):
    """
    Computes the state of charge of the battery.
    """
    if t == m.time[1]:  # TODO: Are we sure this should not be m.time[0]?
        return m.battery_soc[t, u] == m.battery_soc[m.time[-1], u]
    else:
        return m.battery_soc[t, u] == (
                m.battery_soc[t - pd.Timedelta(minutes=frequency), u] +
                self._inputs.efficiency_charge * m.battery_inflow[t, u] -
                m.battery_outflow[t, u] / self._inputs.efficiency_discharge
        )


def state_of_charge_limit(m, t, u):
    """
    Limits the maximum state of charge to the capacity of the battery.
    """
    return m.battery_soc[t, u] <= m.optimal_capacity[u, 'b']


def limit_inflow(m, t, u):
    """
    Limits the battery inflow.
    """
    return m.battery_inflow[t, u] <= m.optimal_capacity[u, 'b'] / self._inputs.charge_rate


def limit_outflow(m, t, u):
    """
    Limits the battery inflow.
    """
    return m.battery_outflow[t, u] <= m.optimal_capacity[u, 'b'] / self._inputs.discharge_rate


def energy_balance(m, t, u):
    """
    Energy balance of the REC.
    """
    return (
            self._inputs.demand.loc[t, u] +
            m.exports_retailer[t, u] +
            m.exports_rec[t, u] +
            m.electricity_consumed[t, u]
            ==
            m.pv_generation[t, u] +
            m.battery_outflow[t, u] +
            m.imports_retailer[t, u] +
            m.imports_rec[t, u]
    )


def local_exchanges(m, t):
    """
    Ensures that exports to the REC are equal to imports from the REC.
    """
    return (
            pyo.quicksum(m.exports_rec[t, u] for u in m.member)
            ==
            pyo.quicksum(m.imports_rec[t, u] for u in m.member)
    )


def limit_exports(m, t, u):
    """
    Limits the total exports to the electricity produced.
    """
    return m.exports_rec[t, u] + m.exports_retailer[t, u] <= m.electricity_produced[t, u]
