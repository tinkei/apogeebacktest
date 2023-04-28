from abc import ABC


class Connector(ABC):
    """An abstract base class for data connections."""

    def __init__(self, name:str, **kwargs) -> None:
        """Constructor.

        Parameters
        ----------
        name : str
            The name of the connector. Must be unique within a `Market`.
        """
        super(Connector, self).__init__()
        self._name = name


    @property
    def name(self):
        """Name of the connector."""
        return self._name
