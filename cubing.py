#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Events whose "best (single)" is treated as record
EVENTS_BEST    = ['333bf', '444bf', '555bf', '333mbf']
# Events whose "average" is treated as record
EVENTS_AVERAGE = ['333', '333female', '444', '555', '222', '333oh', '333ft', '333fm', 'minx', 'pyram',
                  'sq1', 'clock', 'skewb', '666', '777']
# All events
EVENTS_ALL = EVENTS_BEST + EVENTS_AVERAGE

# Full events name
EVENTS_NAME = {
    '333'   : "3x3 Cube",
    '333female': "3x3 Cube (Female)",
    '444'   : "4x4 Cube",
    '555'   : "5x5 Cube",
    '222'   : "2x2 Cube",
    '333bf' : "3x3 Cube: Blindfolded",
    '333oh' : "3x3 Cube: One-handed",
    '333fm' : "3x3 Cube: Fewest moves",
    '333ft' : "3x3 Cube: With feet",
    'minx'  : "Megaminx",
    'pyram' : "Pyraminx",
    'sq1'   : "Square-1",
    'clock' : "Rubik's Clock",
    'skewb' : "Skewb",
    '666'   : "6x6 Cube",
    '777'   : "7x7 Cube",
    '444bf' : "4x4 Cube: Blindfolded",
    '555bf' : "5x5 Cube: Blindfolded",
    '333mbf': "3x3 Cube: Multiple Blindfolded"
}

def format_record(record, event):
    """ Format record value to formatted string suitable for the event. """
    if event == '333fm':
        return str(record)[0:2] + '.' + str(record)[2:]
    elif event == '333mbf':
        # Skip old multiple-bf format
        if 1000000000 < record:
            return str(record)
        else:
            record = str(record)
            diff = 99 - int(record[0:2])
            sec  = int(record[2:7])
            miss = int(record[7:9])
            solved = diff + miss
            attempted = solved + miss
            return '%d/%d (%d:%02d)' % (solved, attempted, sec / 60, sec % 60)
    else:
        msec, _sec = record % 100, record / 100
        sec, min = _sec % 60, _sec / 60
        if 0 < min:
            return '%d:%02d.%02d' % (min, sec, msec)
        else:
            return '%d.%02d' % (sec, msec)

