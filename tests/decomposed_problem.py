import os
import unittest


@given()
def unitest():


class Decomposed(unittest.TestCase):
    def setUp(self):
        # Set the working directory to the root.
        os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    def model_decomposition(self):

        # path = 'instances'
        # json_file = 'example_test.json'
        #
        # system_configuration = SimulationConfiguration(path_input=os.path.join(path, json_file))
        # system_configuration.load()
        # agent_dam = DAM()
        # agent_dam.initialise(system_configuration)
        #
        # self.assertAlmostEqual(float(agent_dam.prices['2016-01-01 15:00:00':'2016-01-01 23:00:00'].sum()), 251.91)
        # self.assertAlmostEqual(float(agent_dam.prices['2017-07-07 00:00:00':'2017-08-08 23:00:00'].sum()), 25462.27)
        # self.assertAlmostEqual(float(agent_dam.prices['2017-01-07 00:00:00':'2017-01-08 23:00:00'].sum()), 2500.72)
