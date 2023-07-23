__all__ = [
    'ContactIdMessage',
    'Message',
    'PARSER_MAPPING',
    'SIAMessage',
]

from open_alarm_monitor.protocols.contact_id import ContactIdMessage
from open_alarm_monitor.protocols.message import Message
from open_alarm_monitor.protocols.sia import SIAMessage

PARSER_MAPPING = {
    'contact_id': ContactIdMessage,
    'sia': SIAMessage,
}
