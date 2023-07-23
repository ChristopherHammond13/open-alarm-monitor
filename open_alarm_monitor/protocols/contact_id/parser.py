"""Open Alarm Monitor: ContactID Protocol Message Parser.

This file provides a ContactIdMessage class that can parse and represent
the contents of a ContactID message.
"""
from binascii import hexlify
from logging import Logger

from open_alarm_monitor.protocols.contact_id.constants import (
    EVENTS,
    QUALIFIERS,
)
from open_alarm_monitor.protocols.message import Message


class ContactIdMessage(Message):
    """Parser for a Contact ID Message."""
    def __init__(self):
        logger = Logger("open_alarm_monitor.protocols.ContactID")
        super().__init__(logger=logger)

    def parse_message(self, message: str) -> None:
        """Parse a Contact ID Message."""
        super().parse_message(message)
        if len(message) != 16:
            self.logger.error(
                "Received a ContactID alarm panel message with an unexpected size. "
                f"Expected: 16, received: {len(message)}"
            )
            print(str(hexlify(message)))
            return

        if (
            message[4:6] != b'18' and
            message[4:6] != b'98'
        ):
            # This is not a valid ContactID message
            self.logger.error(
                "Received a message that does not look like a ContactID one. "
                f"Indicated message type: {message[4:6]}"
            )
            return

        # Parse out the fields of the message
        account = int(message[0:4].decode('ascii').replace('A', '0'))
        try:
            # Single digit qualifier
            qualifier = int(message[6:7])
            # Three digit event code
            event = int(message[7:10])
            # Two digit partition number
            partition = int(message[10:12])
            # Value
            value = int(message[12:15])

        except ValueError:
            self.logger.error("Value error; failed to parse message body.")
            return

        try:
            qualifier_str = QUALIFIERS[qualifier]
        except KeyError:
            qualifier_str = "Unknown Qualifier"
            self.logger.warning(f"Parsed an unknown qualifier: {qualifier}")

        try:
            event_str = EVENTS[event]
        except KeyError:
            event_str = "Unknown event code"
            self.logger.warning(f"Parsed an unknown event code: {event}")

        self.account_number = account
        self.area = partition
        self.event = f"{event_str} {qualifier_str}"
        self.description = f"{event_str} {qualifier_str}"
        self.value = value
        self.value_affects = 'Zone/User'
