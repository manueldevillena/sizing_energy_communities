import itertools

from sizing.utils import read_inputs, set_file_to_object

DEFAULT_ATTR = 0


class OptimisationInputs:
    """
    Object gathering all the inputs for the different optimisation problems.
    """

    def __init__(self, input_parameters: str, input_files: str, output_path: str):
        """
        Constructor.
        """
        self.stochastic = None
        input_parameters = read_inputs(input_parameters)

        # Mandatory attributes
        for attr in [
            'interest_rate', 'discount_rate', 'lifetime', 'efficiency_charge', 'efficiency_discharge', 'charge_rate',
            'discharge_rate'
        ]:
            try:
                setattr(self, attr, input_parameters[attr])
            except KeyError:
                raise KeyError('Attribute "{}" is mandatory in the configuration file.'.format(attr))

        # Optional attributes
        for attr in [
            'stochastic'
        ]:
            try:
                setattr(self, attr, input_parameters[attr])
            except KeyError:
                pass

        # Mandatory files
        if self.stochastic:
            number_scenarios = len(self.stochastic)
            files_demand = ['demand_scenario_{}'.format(i) for i in range(1, number_scenarios+1)]
            files_generation = ['generation_scenario_{}'.format(i) for i in range(1, number_scenarios+1)]
            for file in itertools.chain(*[files_demand, files_generation]):
                try:
                    set_file_to_object(self, input_files, file)
                except FileNotFoundError:
                    raise FileNotFoundError('File "{}.csv" is mandatory and was not found in the inputs.'.format(file))
        else:
            for file in [
                'demand', 'generation'
            ]:
                try:
                    set_file_to_object(self, input_files, file)
                except FileNotFoundError:
                    raise FileNotFoundError('File "{}.csv" is mandatory and was not found in the inputs.'.format(file))

        # Optional files
        for file in [
            'prices_grid_import', 'prices_grid_export', 'prices_community_import', 'prices_community_export',
            'cost_technology_investment', 'cost_technology_running_fixed', 'cost_technology_running_variable',
            'initial_capacity'
        ]:
            try:
                set_file_to_object(self, input_files, file)
            except FileNotFoundError:
                setattr(self, file, DEFAULT_ATTR)

        self.output_path: str = output_path
