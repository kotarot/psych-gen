#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cubing

from jinja2 import Environment, FileSystemLoader


COMPETITORS_FILENAME = 'competitors.txt'
EVENTS_FILENAME      = 'events.txt'
WCARESULTS_FILENAME  = 'WCA_export_Results.tsv'
PSYCH_TEMPLATE       = 'psych.tpl'
PSYCH_HTML           = 'psych.html'


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
                if event_id in cubing.EVENTS_BEST:
                    record = int(best)
                elif event_id in cubing.EVENTS_AVERAGE:
                    record = int(average)
                if 0 < record:
                    # Store the record
                    if (person_id not in raw[event_id]) or (record < raw[event_id][person_id]['value']):
                        raw[event_id][person_id] = {'value': record,
                                                    'formatted': cubing.format_record(record, event_id),
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
    html = tpl.render({'competition_name': 'CompetitionName', 'events_name': cubing.EVENTS_NAME,
                       'events': events, 'psych': psych})
    with open(PSYCH_HTML, 'w') as f:
        f.write(html.encode('utf-8'))
    print 'Complete writing to %s' % (PSYCH_HTML)
