"""Open Alarm Monitor: Generic Message Class.

This file contains a base class for a parser that takes a message from an alarm, parses it,
and sets us up to do something useful with it.
"""
from abc import (
    ABC,
    abstractmethod,
)
from binascii import hexlify
from logging import Logger
from typing import Optional


class Message(ABC):
    def __init__(self, logger: Logger = Logger("open_alarm_monitor.protocols.generic_message")):
        """Set up an empty message."""
        self.account_number: Optional[int] = None
        self.area: Optional[int] = None
        self.event: Optional[str] = None
        self.description: Optional[str] = None
        self.value: Optional[int] = None
        self.value_affects: Optional[str] = None
        self.extra_text: Optional[str] = None

        self.logger: Logger = logger

    @abstractmethod
    def parse_message(self, message: bytes) -> None:
        print("Parsing message received from panel: " + str(hexlify(message)))
