"""Open Alarm Monitor: Account Management."""
from typing import List

from open_alarm_monitor.handlers.handler import MessageHandler
from open_alarm_monitor.protocols import PARSER_MAPPING


class Account:
    """Each account corresponds to one alarm."""
    def __init__(
            self,
            name: str,
            address: str,
            protocol: str,
            account_number: int,
            polling_interval: int = 2,
    ):
        self.name = name
        self.address = address
        self.account_number = account_number
        self.polling_interval = polling_interval

        if protocol in PARSER_MAPPING.keys():
            self.protocol_name = protocol
            self.parser = PARSER_MAPPING[protocol]
        else:
            raise Exception(f"Unknown protocol specified for account {name}: {protocol}")

        self.handlers: List[MessageHandler] = []

    def handle_message(self, message: str):
        for handler in self.handlers:
            handler.handle(account=self, message=message)

    def __str__(self) -> str:
        return f"{self.name} (#{self.account_number})"

    def __repr__(self) -> str:
        return f"{self.name}_{self.account_number}"
