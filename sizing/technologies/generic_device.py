from abc import ABC

from sizing.core import OptimisationInputs


class GenericDevice(ABC):
    """
    Generic class containing generic methods shared across devices.
    """
    def __init__(self, inputs: OptimisationInputs, model: PyomoModel):
        """
        Constructor.
        """
        self._inputs = inputs
        self._model = model
