# Open Alarm Monitor
Python 3 implementation of an Alarm Receiving Centre (ARC), with a focus on Texecom panels (and clean code).

This is effectively a reimplemnentation of much of the [excellent work done by @mikestir](https://github.com/mikestir/alarm-server/blob/master/alarmrx.py) around five years ago, but with extensibility (such as custom shell execution and a Twilio integration).

Texecom supports two protocols: ContactID and SIA. This application should support both.

## Get Started

Copy `config.example.toml` to `config.toml` and fill in the gaps. Then, run `alarm_monitor listen` to get the server online.

## Message Structures

### ContactID

*Note that this documentation is based on this document: https://www.voip-sip-sdk.com/attachments/583/contact_id.pdf*

ContactID messages are 16 bytes in length, and there are four possible structures (that are all quite similar).

All messages start with some common data, namely the four digit account number; the two digit Contact ID code (18); and a four digit event qualifier (contextual). All events also end in a single byte (0 - F) checksum.

#### Checksum Algorithm

1. Add all of the message digits up, using the number itself for 1 - 9, and adding 10 for each zero.
2. Find the next highest multiple of 15.
3. Subtract the sum from this value.
4. Use the result for the checksum, substituting 0 for F. (e.g., 0 = F, 1 = 1, 2 = 2, ..., 14 = E)

#### Structure 1: Alarm Message

Note that spaces are for clarity, and should be ignored.
```plaintext
AAAA II QQQQ PP ZZZ C
```

This can be interpreted as follows:

```plaintext
AAAA = Account Number (e.g., 1234)
II   = Message type. Contact ID messages are always either 18 (legacy) or 98 (new).
QQQQ = Event Qualifier. Example: 1131 = 1 (for burglary), followed by 131 for a perimeter burglary.
PP   = Partition number (e.g., 01)
ZZZ  = Zone number (e.g., 015)
C    = Checksum (e.g., 8)
```

`1234 18 1131 01 015 8` would therefore mean that:
- [1234] Account 1234
- [ 18 ] is sending a Contact ID message
- [1131] indicating a perimeter burglary
- [ 01 ] in the first partition of the building
- [ 015] triggerd by Zone 15
- [   8] with checksum 8

#### Structure 2: Restore Message

This is sent when the alarm is reset.

The structure is the same, except that the first Qualifier digit is `3` instead of `1`, indicating a restore. Example message:

```plaintext
1234 18 3131 01 015 6
```

#### Structure 3: Opening Message

This message type is sent when an alarm is disarmed. The structure is:

```plaintext
AAAA II QQQQ PP UUU C

QQQQ = Event Qualifier, e.g., 1 for an opening, followed by the event code for a user open (401)
UUU  = The User number, e.g., 003

Example:
1234 18 1401 02 003 5
```

#### Structure 4: Closing Message

This message type is sent when an alarm is armed.

```plaintext
AAAA II QQQQ PP UUU C

QQQQ = Event Qualifier, e.g., 3 for a closing, followed by the event code for a user open (401)
UUU  = The User number, e.g., 003

Example:
1234 18 3401 03 005 F
```
