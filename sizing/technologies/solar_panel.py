import pyomo.environ as pyo

from . import GenericDevice
from sizing.core import OptimisationInputs


class SolarPanel(GenericDevice):
    """
    Collection of methods associated to solar panel generation
    """
    def __init__(self, inputs: OptimisationInputs, model):
        """
        Constuctor.
        """
        super().__init__(inputs, model)

    def pv_generation(self):
        """
        Computes the electricity generation of the solar panel array.
        """
        self._model.pv_generation_eqn = pyo.ConstraintList()
        for t in self._model.time:
            for u in self._model.members:
                self._model.pv_generation_eqn.add(
                    self._model.pv_geeration[t, u] == (
                            self._inputs.generation.loc[t, u] * self._model.optimal_capacity[u, 'p']
                    )
                )
