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
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(conn_details)
s.settimeout(2)

# Testing with account number 1001
# msg = b'\x01\x00\x00\x01\x01\x08\x01\x01\x03\x01\x00\x01\x00\x01\x01'
msg = b'21001181131011015\r\n'
# msg = bytearray([2, 1, 0, 0, 1, 1, 8, 1, 1, 0, 3, 1, 0, 1, 0, 1, 1, 5, ord(b'\r'), ord(b'\n')])
# msg = b


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


# msg += checksum(msg).to_bytes(length=1, byteorder='big') + b'\r\n'
# print(msg)
# s.send(msg)
# msg += b'\r\n'
print(msg)
s.send(msg)
s.close()
