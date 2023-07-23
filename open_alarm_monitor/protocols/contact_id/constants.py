"""Open Alarm Monitor: ContactID Protocol.

This file contains a mapping between ContactID codes and human-readable meanings.
"""
QUALIFIERS = {
    1: 'Event/Activates',
    3: 'Restore/Secured',
    6: 'Status',
}

EVENTS = {
    100: 'Medical',
    110: 'Fire',
    120: 'Panic',
    121: 'Duress',
    122: 'Silent Attack',
    123: 'Audible Attack',
    130: 'Intruder',
    131: 'Perimeter',
    132: 'Interior',
    133: '24 Hour',
    134: 'Entry/Exit',
    135: 'Day/Night',
    136: 'Outdoor',
    137: 'Zone Tamper',
    139: 'Confirmed Alarm',
    145: 'System Tamper',

    300: 'System Trouble',
    301: 'AC Lost',
    302: 'Low Battery',
    305: 'System Power Up',
    320: 'Mains Over-voltage',
    333: 'Network Failure',
    351: 'ATS Path Fault',
    354: 'Failed to Communicate',

    400: 'Arm/Disarm',
    401: 'Arm/Disarm by User',
    403: 'Automatic Arm/Disarm',
    406: 'Alarm Abort',
    407: 'Remote Arm/Disarm',
    408: 'Quick Arm',

    411: 'Download Start',
    412: 'Download End',
    441: 'Part Arm',

    457: 'Exit Error',
    459: 'Recent Closing',
    570: 'Zone Locked Out',

    601: 'Manual Test',
    602: 'Periodic Test',
    607: 'User Walk Test',

    623: 'Log Capacity Alert',
    625: 'Date/Time Changed',
    627: 'Program Mode Entry',
    628: 'Program Mode Exit',
}
