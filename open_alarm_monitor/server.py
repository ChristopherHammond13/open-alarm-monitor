"""Open Alarm Monitor: TCP Server.

This file contains the server that listens for data from the alarm.
"""
import logging
import socketserver

from binascii import hexlify
from typing import Dict

from open_alarm_monitor.accounts import Account
from open_alarm_monitor.protocols import ContactIdMessage
from open_alarm_monitor.protocols import SIAMessage


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


ACCOUNTS: Dict[int, Account] = {}
LOGGER = logging.Logger("SocketServer")


class AlarmMessageHandler(socketserver.BaseRequestHandler):
    def error(self, msg):
        LOGGER.error(msg, extra={'tag': self.client_address[0]})

    def info(self, msg):
        LOGGER.info(msg, extra={'tag': self.client_address[0]})

    def debug(self, msg):
        LOGGER.debug(msg, extra={'tag': self.client_address[0]})

    # POLL flags (not all of these are verified - see docs)
    FLAG_LINE_FAILURE = 1
    FLAG_AC_FAILURE = 2
    FLAG_BATTERY_FAILURE = 4
    FLAG_ARMED = 8
    FLAG_ENGINEER = 16

    def handle_poll(self, data):
        self.debug("%s" % (data))

        try:
            parts = (data[4:].decode('ascii')).strip().split('#')
            account_number = int(parts[0])
            flags = ord(parts[1][0])
        except Exception as e:
            self.error("POLL parse error: " + str(e))
            return

        self.info("Poll for account %d with flags 0x%02x" % (account_number, flags))

        # # Check we recognise the account number and that the client IP matches
        # if self.server.account_manager.get_ip(account) != self.client_address[0]:
        #     self.error("Invalid IP address for account %s" % (account))
        #     return

        # Send ack/polling delay in minutes
        account = ACCOUNTS.get(account_number)
        if not account:
            self.error(f"Received a message for an unknown account (#{account_number})")
            return

        self.request.send(b'[P]\x00' + bytes([account.polling_interval]) + b'\x06\r\n')

        ac_failure = (flags & self.FLAG_AC_FAILURE) > 0
        armed = (flags & self.FLAG_ARMED) > 0
        battery_failure = (flags & self.FLAG_BATTERY_FAILURE) > 0
        engineer = (flags & self.FLAG_ENGINEER) > 0
        line_failure = (flags & self.FLAG_LINE_FAILURE) > 0

        poll_message = (
            f"ac_failure={ac_failure}|armed={armed}|battery_failure={battery_failure}|"
            f"engineer={engineer}|line_failure={line_failure}"
        )

        account.handle_message(poll_message)

    def handle_message(self, data, parser):
        # Parse message
        # message = parser(self.client_address[0], data[1:])

        # We strip away the single digit Texecom prefix
        data = data[1:]

        if parser == 'contact_id':
            message = ContactIdMessage()
            message.parse_message(data)
        elif parser == 'sia':
            message = SIAMessage()
            message.parse_message(data)
        else:
            raise Exception("Unknown message type")

        self.info(
            "%s: a/c %s area %d %s %s %d %s" % (
                type(message).__name__,
                message.account_number,
                message.area,
                message.event,
                message.value_affects,
                message.value,
                message.extra_text
            )
        )
        if message.description:
            self.debug(message.description)

        # Send ACK
        self.request.send(data[0:1] + b'\x06\r\n')

        plaintext_message = (
            f"area={message.area}|event={message.event}|value={message.value}|"
            f"value_affects={message.value_affects}|extra_text={message.extra_text}"
        )

        account = ACCOUNTS[message.account_number]
        account.handle_message(plaintext_message)

    def handle(self):
        self.debug("Client connected from %s:%s" % (self.client_address[0], self.client_address[1]))

        while True:
            data = self.request.recv(1024)
            if not data:
                break

            # Dump raw packet
            self.debug('RAW: %s' % (hexlify(data)))

            if data[0:3] == b'+++':
                # End of transmission - we'll got a TCP disconnection after this
                # so just ignore this silently
                continue

            # All other messages should have <CR><LF> terminator which we can remove
            if data[-2:] != b'\r\n':
                self.error("Ignoring line with missing terminator")
                continue
            data = data[:-2]

            # Determine packet type and pass to handler
            if data[0:4] == b'POLL':
                # Polling packet
                self.handle_poll(data)
            elif data[0:1] == b'2':
                self.handle_message(data, 'contact_id')
            elif data[0:1] == b'3':
                self.handle_message(data, 'sia')
            else:
                self.error("Unhandled message: %s" % (hexlify(data)))

        self.debug("Client disconnected")
        self.request.close()


class AlarmServer:
    def __init__(self, listen_address: str, listen_port: int):
        self.listen_address = listen_address
        self.listen_port = listen_port

    def listen(self):
        self.server = ThreadedTCPServer(
            (self.listen_address, self.listen_port),
            AlarmMessageHandler,
        )
        self.server.allow_reuse_address = True
        self.server.allow_reuse_port = True

        with self.server:
            ip, port = self.server.server_address
            print(f"Listening on {ip}:{port}")
            self.server.serve_forever()
