__all__ = ['HANDLERS']

from typing import Dict
from open_alarm_monitor.handlers.handler import MessageHandler
from open_alarm_monitor.handlers.shell_exec import ShellExecMessageHandler
from open_alarm_monitor.handlers.twilio_voice import TwilioVoiceMessageHandler

HANDLERS: Dict[str, MessageHandler] = {
    "shell_exec": ShellExecMessageHandler,
    "twilio_voice": TwilioVoiceMessageHandler,
}
