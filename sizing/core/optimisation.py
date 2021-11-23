import pyomo.environ as pyo

import sizing.constraints.constraints as cs
from sizing import models
from sizing.core import OptimisationInputs

from sizing.models import list_constraints

class Optimisation:
    """
    Driver running the simulation.
    """
    def __init__(self, inputs: OptimisationInputs):
        """
        Constructor.
        """
        self.model = pyo.ConcreteModel()
        self._model_structure = models.ModelStructure(inputs)

    def create_problem(self):
        """
        Initialises the problem.
        """
        self._model_structure.initialise_problem(self.model)

    def instantiate_problem(self):
        """
        Instantiate the problem.
        """
        map_string_index = {
            'member': self.model.member,
            'time': self.model.time
        }

        for name, constraint in list_constraints.items():
            if len(constraint) == 1:
                self.model.add_component(name, pyo.Constraint(rule=constraint))
            else:
                self.model.add_component(
                    name, pyo.Constraint(*(map_string_index[i] for i in constraint[:-1]), rule=constraint)
                )

        self.model.objective_eqn = pyo.Objective(rule=cs.objective_function, sense=pyo.minimize)
        self.model._total_costs_eqn = pyo.Constraint(self.model.member, rule=cs.total_costs)
        self.model._annual_investments_eqn = pyo.Constraint(self.model.member, rule=cs.annual_investments)
        self.model._annual_operational_costs_eqn = pyo.Constraint(self.model.member, rule=cs.annual_operational_costs)
        self.model._annual_electricity_bills_eqn = pyo.Constraint(self.model.member, rule=cs.annual_electricity_bills)
        self.model._annual_electricity_revenue_eqn = pyo.Constraint(self.model.member, rule=cs.annual_electricity_revenue)
        self.model._technology_consumption_eqn = pyo.Constraint(self.model.time, self.model.member, rule=cs.technology_consumption)
        self.model._state_of_charge_eqn = pyo.Constraint(self.model.time, self.model.member, rule=cs.state_of_charge)
        self.model._state_of_charge_limit_eqn = pyo.Constraint(self.model.time, self.model.member, rule=cs.state_of_charge_limit)
        self.model._limit_inflow_eqn = pyo.Constraint(self.model.time, self.model.member, rule=cs.limit_inflow)
        self.model._limit_outflow_eqn = pyo.Constraint(self.model.time, self.model.member, rule=cs.limit_outflow)
        self.model._energy_balance_eqn = pyo.Constraint(self.model.time, self.model.member, rule=cs.energy_balance)
        self.model._local_exchanges_eqn = pyo.Constraint(self.model.time, rule=cs.local_exchanges)

    def solve_problem(self):
        """
        Solves the problem.
        """
        pass