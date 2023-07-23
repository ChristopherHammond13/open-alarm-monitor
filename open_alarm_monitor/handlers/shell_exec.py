"""Open Alarm Monitor: Shell Execution Handler.

WARNING: USE WITH CARE AS THIS MAY OPEN YOU UP TO DANGER.

This file contains an implementation of a basic shell script runner that passes in relevant
arguments when a message comes from the alarm.
"""
import subprocess

from typing import TYPE_CHECKING

from open_alarm_monitor.handlers.handler import MessageHandler

if TYPE_CHECKING:
    from open_alarm_monitor.accounts import Account


class ShellExecMessageHandler(MessageHandler):
    def handle(self, account: 'Account', message):
        base_command = self.config['command']
        args = [
            base_command,
            str(account.account_number),
            message,
        ]

        subprocess.Popen(args)

        return super().handle(account, message)
