#!/usr/bin/env python
# -*- coding: utf-8 -*-

from jinja2 import Environment, FileSystemLoader

COMPETITORS_FILENAME = 'competitors.txt'
EVENTS_FILENAME      = 'events.txt'
WCARESULTS_FILENAME  = 'WCA_export_Results.tsv'
PSYCH_TEMPLATE       = 'psych.tpl'
PSYCH_HTML           = 'psych.html'

# Events whose "best (single)" is treated as record
EVENTS_BEST    = ['333bf', '333fm', '444bf', '555bf', '333mbf']
# Events whose "average" is treated as record
EVENTS_AVERAGE = ['333', '444', '555', '222', '333oh', '333ft', 'minx', 'pyram',
                  'sq1', 'clock', 'skewb', '666', '777']
# Full events name
EVENTS_NAME = {
    '333'   : "Rubik's Cube",
    '444'   : "4x4 Cube",
    '555'   : "5x5 Cube",
    '222'   : "2x2 Cube",
    '333bf' : "Rubik's Cube: Blindfolded",
    '333oh' : "Rubik's Cube: One-handed",
    '333fm' : "Rubik's Cube: Fewest moves",
    '333ft' : "Rubik's Cube: With feet",
    'minx'  : "Megaminx",
    'pyram' : "Pyraminx",
    'sq1'   : "Square-1",
    'clock' : "Rubik's Clock",
    'skewb' : "Skewb",
    '666'   : "6x6 Cube",
    '777'   : "7x7 Cube",
    '444bf' : "4x4 Cube: Blindfolded",
    '555bf' : "5x5 Cube: Blindfolded",
    '333mbf': "Rubik's Cube: Multiple Blindfolded"
}


def read_competitors():
    """ Reads competitors list from file. """
    ret = []
    with open(COMPETITORS_FILENAME, 'r') as f:
        for line in f:
            ret.append(line.replace('\r', '').replace('\n', ''))
    return ret


def read_events():
    """ Reads events list from file. """
    ret = []
    with open(EVENTS_FILENAME, 'r') as f:
        for line in f:
            ret.append(line.replace('\r', '').replace('\n', ''))
    return ret


def read_wcaresults(competitors, events):
    """ Reads the WCA results. Returns data for psych sheets. """

    # Initialization with events
    raw = {}
    for e in events:
        raw[e] = {}

    # Read raw data
    with open(WCARESULTS_FILENAME, 'r') as f:
        next(f)
        for line in f:
            items = line.split('\t')
            event_id, best, average, person_name, person_id = items[1], items[4], items[5], items[6], items[7]
            if (event_id in events) and (person_id in competitors):
                record = -1
                if event_id in EVENTS_BEST:
                    record = int(best)
                elif event_id in EVENTS_AVERAGE:
                    record = int(average)
                if 0 < record:
                    # Store the record
                    if (person_id not in raw[event_id]) or (record < raw[event_id][person_id]['value']):
                        raw[event_id][person_id] = {'value': record,
                                                    'formatted': format_record(record, event_id),
                                                    'id': person_id, 'name': person_name.decode('utf-8')}

    # Sort by record
    psych = {}
    for ek, ev in raw.items():
        psych[ek] = []
        print 'In the event of %s......' % (ek)
        for k, v in sorted(ev.items(), key=lambda x:x[1]['value']):
            psych[ek].append(v)
            print '  %s achieves %s' % (k, v['formatted'])

    return psych


def format_record(record, event):
    """ Format record value to formatted string suitable for the event. """
    if event == '333fm':
        return str(record)
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


if __name__ == '__main__':
    # Read competitors and events
    competitors = read_competitors()
    events = read_events()
    print 'competitors:', competitors
    print 'events:', events

    # Read WCA results and store them
    psych = read_wcaresults(competitors, events)
    #print 'psych: ', psych

    # Generate html
    env = Environment(loader=FileSystemLoader('./', encoding='utf8'))
    tpl = env.get_template(PSYCH_TEMPLATE)
    html = tpl.render({'competition_name': 'CompetitionName', 'events_name': EVENTS_NAME,
                       'events': events, 'psych': psych})
    with open(PSYCH_HTML, 'w') as f:
        f.write(html.encode('utf-8'))
    print 'Complete writing to %s' % (PSYCH_HTML)
