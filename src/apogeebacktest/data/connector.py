from abc import ABC


class Connector(ABC):
    """An abstract base class for data connections."""

    def __init__(self, **kwargs) -> None:
        super(Connector, self).__init__()
