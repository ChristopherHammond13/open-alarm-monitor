"""Open Alarm Monitor: Base Message Handler."""

from abc import (
    ABC,
    abstractmethod,
)
from typing import TYPE_CHECKING


# Ensure we do not cause a circular import
if TYPE_CHECKING:
    from open_alarm_monitor.accounts import Account


class MessageHandler(ABC):
    """Abstract base class representing a message handler."""

    def __init__(self, config: dict):
        self.config = config

    @abstractmethod
    def handle(self, account: 'Account', message):
        pass
