import pandas as pd

from sizing.utils import read_data, read_inputs


class OptimisationInputs:
    """
    Object gathering all the inputs for the different optimisation problems.
    """

    def __init__(self, demand_members_path: str, production_members_path: str, prices_import_grid_members_path: str,
                 prices_import_local_members_path: str, prices_export_grid_members_path: str,
                 prices_export_local_members_path: str, initial_capacity_path: str, cost_technology_path: str,
                 cost_technology_running_fixed_path: str, additional_inputs_path: str, output_path: str):
        """
        Constructor.
        """
        self.demand_members: pd.DataFrame = read_data(demand_members_path)
        self.production_members: pd.DataFrame = read_data(production_members_path)
        self.prices_import_grid_members: pd.DataFrame = read_data(prices_import_grid_members_path)
        self.prices_import_local_members: pd.DataFrame = read_data(prices_import_local_members_path)
        self.prices_export_grid_members: pd.DataFrame = read_data(prices_export_grid_members_path)
        self.prices_export_local_members: pd.DataFrame = read_data(prices_export_local_members_path)
        self.initial_capacity: pd.DataFrame = read_data(initial_capacity_path)
        self.cost_technology: pd.DataFrame = read_data(cost_technology_path)
        self.cost_technology_running_fixed: pd.DataFrame = read_data(cost_technology_running_fixed_path)
        self.output_path: str = output_path

        inputs = read_inputs(additional_inputs_path)
        # Mandatory attributes
        for attr in [
            'interest_rate', 'discount_rate', 'lifetime', 'efficiency_charge', 'efficiency_discharge', 'charge_rate',
            'discharge_rate'
        ]:
            try:
                setattr(self, attr, inputs[attr])
            except KeyError:
                raise KeyError('Attribute "{}" is mandatory in the configuration file.'.format(attr))

        self.cost_technology_running_variable = 0
