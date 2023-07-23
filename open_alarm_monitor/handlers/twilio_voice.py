"""Open Alarm Monitor: Twilio Voice.

This file uses the Twilio API to call up a verified phone number when the alarm triggers.
"""
from typing import TYPE_CHECKING

from twilio.rest import Client as TwilioClient
from twilio.twiml.voice_response import VoiceResponse

from open_alarm_monitor.handlers.handler import MessageHandler

if TYPE_CHECKING:
    from open_alarm_monitor.accounts import Account


def ordinal(n: int):
    if 11 <= (n % 100) <= 13:
        suffix = 'th'
    else:
        suffix = ['th', 'st', 'nd', 'rd', 'th'][min(n % 10, 4)]
    return str(n) + suffix


class TwilioVoiceMessageHandler(MessageHandler):
    def handle(self, account: 'Account', message: str):
        super().handle(account, message)

        parts = message.split('|')
        message_dict = {}
        for part in parts:
            k, v = part.split('=')
            message_dict[k] = v

        if 'Activate' not in message_dict['event']:
            # The alarm did not go off
            return

        print("Alarm activated! Initiating phone call.")
        client = TwilioClient(
            self.config['account_sid'],
            self.config['auth_token'],
        )

        sentence = (
            f"The alarm has been triggered in the {ordinal(int(message_dict['area']))} zone. "
            f"It originated from sensor number {message_dict['value']}."
        )
        response = VoiceResponse()
        response.say(sentence, loop=0)

        print("Executing TwiML")
        print(response)
        call = client.calls.create(
            twiml=response,
            to=self.config['target_phone_number'],
            from_=self.config['account_phone_number'],
        )
        print(call.sid)
