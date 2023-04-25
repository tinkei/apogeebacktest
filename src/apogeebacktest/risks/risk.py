from abc import ABC, abstractmethod


class RiskMetric(ABC):
    """An abstract base class for measuring investment risk."""

    def __init__(self, **kwargs) -> None:
        super(RiskMetric, self).__init__()
