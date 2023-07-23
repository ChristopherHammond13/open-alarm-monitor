#!/usr/bin/env python3
import socket
try:
    # This is native on Python 3.11
    import tomllib
except ImportError:
    import tomli as tomllib


with open('config.toml', 'rb') as f:
    config = tomllib.load(f)

listen_data = config['open_alarm_monitor']['listen']
conn_details = ("localhost", int(listen_data['port']))
# conn_details = (listen_data['address'], int(listen_data['port']))
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(conn_details)
s.settimeout(2)

# Testing with account number 1001
# We also prefix the message with a 2 to designate that this is a Texecom event
msg = b'2100118113101101'


def checksum(msg) -> int:
    total = 0
    for num in msg:
        num_int = int(chr(num))
        print(num_int)

        if num_int == 0:
            total += 10
        else:
            total += num_int

    # https://stackoverflow.com/a/11692953
    next_multiple_of_15 = total + 15 - 1
    next_multiple_of_15 -= (next_multiple_of_15 % 15)

    checksum = next_multiple_of_15 - total

    if checksum == 0:
        checksum_str = b'F'
    elif checksum == 10:
        checksum_str = b'A'
    elif checksum == 11:
        checksum_str = b'B'
    elif checksum == 12:
        checksum_str = b'C'
    elif checksum == 13:
        checksum_str = b'D'
    elif checksum == 14:
        checksum_str = b'E'
    else:
        checksum_str = checksum

    print("chk: " + str(checksum_str))
    return checksum_str


msg += checksum(msg[1:]) + b'\r\n'

print(msg)
s.send(msg)
s.close()
