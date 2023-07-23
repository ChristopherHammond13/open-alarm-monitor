"""Open Alarm Monitor: SIA Protocol.

This file contains a mapping between SIA event codes and human-readable meanings.
"""
from functools import reduce
from hexdump import hexdump
from typing import (
    Optional,
    Tuple,
)
from logging import Logger

from open_alarm_monitor.protocols.message import Message
from open_alarm_monitor.protocols.sia.constants import EVENTS


class SIAMessage(Message):
    """Parser for an SIA Format Message."""
    def __init__(self):
        logger = Logger("open_alarm_monitor.protocols.SIAMessage")
        super().__init__(logger=logger)
        self.next_record: Optional['SIAMessage'] = None

    @staticmethod
    def checksum_valid(message: str) -> bool:
        """Verify the message checksum byte."""
        payload_length = message[0] & 0x3f

        checksum = 0xff ^ reduce(
            lambda x, y: x ^ y, message[:3 + payload_length]
        )

        return checksum == 0

    def parse_record(self, message: str) -> Tuple[bytes, bytes, bytes]:
        """Parse a single SIA record, as many may be received in one message."""
        try:
            record_type = message[0] & 0xc0
            payload_length = message[0] & 0x3f
            payload_type = message[1:2]
            payload = message[2 + payload_length]
            next_record = message[3 + payload_length:]
        except IndexError:
            self.logger.error("Failed to parse an SIA message")
            return (b'', b'', b'')

        # Verify checksum
        if not self.checksum_valid(message):
            self.logger.error("SIA message checksum verification failed.")
            return (b'', b'', b'')

        if record_type == 0xc0:
            return (payload_type, payload, next_record)
        else:
            return (b'', b'', next_record)

    def parse_message(self, message: str) -> None:
        """Parse an SIA Format Message."""
        super().parse_message(message)

        while message:
            _type, _payload, message = self.parse_record(message)

            self.logger.debug("%s" % (_type + b' ' + _payload))

            match _type:
                case b'#':
                    self.account_number = _payload.decode('ascii')
                case b'A':
                    self.extra_text = _payload.decode('ascii')
                case b'N':
                    try:
                        area = int(_payload[2:3])
                        event_code = _payload[3:5].decode('ascii')
                        value = int(_payload[5:8])
                    except Exception as e:
                        self.logger.error("Error parsing the payload: ")
                        self.logger.error(hexdump(_payload))
                        self.logger.error(e)

                    self.area = area
                    self.value = value
                    try:
                        sia_event = EVENTS[event_code]
                        self.event = sia_event.name
                        self.description = sia_event.description
                        self.value_affects = sia_event.affects
                    except KeyError:
                        self.logger.error(f"Unknown event code: {event_code}")
