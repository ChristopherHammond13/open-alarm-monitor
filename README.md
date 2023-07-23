# Open Alarm Monitor
Python 3 implementation of an Alarm Receiving Centre (ARC), with a focus on Texecom panels (and clean code).

This is effectively a reimplemnentation of much of the [excellent work done by @mikestir](https://github.com/mikestir/alarm-server/blob/master/alarmrx.py) around five years ago, but with extensibility (such as custom shell execution and a Twilio integration).

Texecom supports two protocols: ContactID and SIA. This application should support both.

## WARNING

This code is in alpha status, and personally solves some use cases for me. This means it may work for you, may not work for you or, worse, may lead you into a false sense of security such that you believe it is working better than it is. I take no responsibility for any losses resulting from this code failing to alert you to an intruder, or failing to meet any other use case you apply it to.

I encourage you to read the code, hack on it, improve it, and let me know if it works for you!

Oh, and since we are dealing with standards published almost 25 years ago, it should go without saying that 'basic' security measures that modern protocols have (like encryption, passwords, etc.) do not exist here. **This code should not be considered secure, and should be run on an offline network where possible. If you must host this outside of your home, employ at very least IP address allow-listing.** Note further that this code allows you to shell execute a script on receipt of an alarm message, so ensure you have guardrails in place there. I recommend against using the shell execution handler, and instead implementing your own and opening a PR against this project to notify the resident to an alarm in some other way.

## Texecom NDA

Some people choose to sign an NDA with Texecom in order to get access to internal documentation; however, I have chosen ***not*** to enter into any such agreement deliberately to ensure that this code can be shared with the community, unencumbered. All the work published in this project is either original (based on reverse engineering), or based on code and reference data available via the Internet (open source). Note further that the Contact ID and SIA specifications are public and cross-vendor.

The code is published under the MIT licence to encourage its adoption and adaptation as the community sees fit.

## Why did I build this?

I wanted my alarm to be able to call me like the 'old days' of traditional diallers. Texecom has several APIs that I have interfaced with in some capacity (including the Wintex one), but implementing an ARC allows you to take advantage of the alarm's native capability to send a message to a server, with retry support, in the event of a major event (such as an alarm state). Eventually, I intend to install a Texecom Premier Elite alarm into my grandmother's home when her POTS phone line is removed as part of her full fibre migration, so that she can take advantage of dialler-like functionality; calling a phone when there is an alarm is much more user-friendly for the elderly than the Texecom Connect app, even without an Openreach / POTS phone line available.

If anybody from Texecom is reading this, the code exists so that I can buy another alarm from you despite owning one myself! Please don't be mad :) Diallers were great, and are a great alternative when one does not wish to pay for a professional ARC/Monitoring service (some of whom charge a fortune and try to convince the elderly they need to spend a lot more on service contracts than they do). There is often no better way to get somebody's attention than just calling their phone.

## Get Started

Copy `config.example.toml` to `config.toml` and fill in the gaps. Then, run `alarm_monitor listen` to get the server online.

## Message Structures

This code technically supports two types of messages: Contact ID and SIA. However, only Contact ID is confirmed working at this point.

### Contact ID

*Note that this documentation is based on this document: https://www.voip-sip-sdk.com/attachments/583/contact_id.pdf*

Contact ID messages are 16 bytes in length, and there are four possible structures (that are all quite similar).

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

### SIA

TODO: document this protocol
