#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cubing

import argparse
import ConfigParser
import csv
import glob
from jinja2 import Environment, FileSystemLoader
import os
import zipfile


SCRIPT_DIR           = os.path.abspath(os.path.dirname(__file__))
WCA_EXPORT_DIR       = '/WCA_export'
WCARESULTS_FILENAME  = 'WCA_export_Results.tsv'
PSYCH_TEMPLATE       = 'psych.tpl'

VALUE_DNF = 9999999999


def read_compinfo(comp):
    """ Reads competition info (name and description) from .txt """
    config = ConfigParser.SafeConfigParser()
    config.read(comp + '.txt')
    return {'name': config.get('competition', 'name'),
            'description': config.get('competition', 'description')}


def read_compdata(comp):
    """ Reads competition data from .csv """
    csvdata, events, competitors, competitorsname, entries = [], [], [], {}, {}

    # Store CSV into dict
    with open(comp + '.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            csvdata.append([item.decode('utf-8').strip() for item in row])

    # Assing ID for new competitors
    n = 1
    for i, row in enumerate(csvdata):
        if row[0] == '0':
            csvdata[i][0] = 'N_%03d' % (n)
            n = n + 1

    # header -> events
    events = [item for item in csvdata[0] if item in cubing.EVENTS_ALL]
    # first column -> competitors
    competitors = [row[0] for row in csvdata[1:]]

    # generate entry info
    for row in csvdata[1:]:
        competitor_id = row[0]
        competitorsname[competitor_id] = row[-1]
        entries[competitor_id] = {}
        for i, flag in enumerate(row[1:-1]):
            if flag != '':
                entries[competitor_id][events[i]] = True
            else:
                entries[competitor_id][events[i]] = False

    return {'events': events, 'competitors': competitors,
            'competitorsname': competitorsname, 'entries': entries}


def find_latest_export():
    """ Finds the latest WCA export in `WCA_export` directory. """
    files = glob.glob(SCRIPT_DIR + WCA_EXPORT_DIR + '/WCA_export*.tsv.zip')
    filesd = {os.path.basename(file)[14:22]: os.path.basename(file) for file in files}
    return filesd.items()[-1][1]


def read_wcaresults(compdata, latest_export):
    """ Reads the WCA results. Returns data for psych sheets. """
    raw = {}

    # Initialization with events
    for event in compdata['events']:
        raw[event] = {}

    # Read raw data
    with zipfile.ZipFile(SCRIPT_DIR + WCA_EXPORT_DIR + '/' + latest_export) as zf:
        with zf.open(WCARESULTS_FILENAME, 'r') as f:
            next(f)
            for line in f:
                items = line.decode('utf-8').split('\t')
                event_id, best, average = items[1], items[4], items[5]
                person_name, person_id = items[6], items[7]
                if (event_id in compdata['events']) and (person_id in compdata['competitors']):
                    compdata['competitorsname'][person_id] = person_name
                    if compdata['entries'][person_id][event_id]:
                        record = -1
                        if event_id in cubing.EVENTS_BEST:
                            record = int(best)
                        elif event_id in cubing.EVENTS_AVERAGE:
                            record = int(average)
                        if (0 < record) and \
                           ((person_id not in raw[event_id]) or (record < raw[event_id][person_id]['value'])):
                            raw[event_id][person_id] = {'id': person_id, 'name': person_name, 'value': record,
                                                        'formatted': cubing.format_record(record, event_id),
                                                        'haswcaid': True}

    # Update new competitors
    for event in compdata['events']:
        for competitor_id, entries in compdata['entries'].items():
            if compdata['entries'][competitor_id][event] and competitor_id not in raw[event]:
                raw[event][competitor_id] = {'id': competitor_id,
                                             'name': compdata['competitorsname'][competitor_id],
                                             'value': VALUE_DNF, 'formatted': '&ndash;',
                                             'haswcaid': competitor_id[0] != 'N'}

    return raw


def generate_psych(wcaresults):
    """ Generates psych data by sorting. """
    psych = {}
    for event_id, event_result in wcaresults.items():
        noobs = {}
        psych[event_id] = []
        print 'In the event of %s......' % (event_id)
        n = 1
        for competitor_id, record in sorted(event_result.items(), key=lambda x:x[1]['value']):
            record['rank'] = n
            if record['value'] < VALUE_DNF:
                psych[event_id].append(record)
                print '  #%d %s achieves %s' % (n, competitor_id, record['formatted'])
                n = n + 1
            else:
                noobs[competitor_id] = record

        for competitor_id, record in sorted(noobs.items(), key=lambda x:x[1]['id']):
            psych[event_id].append(record)
            print '  #%d %s is noob' % (n, competitor_id)

    return psych


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Psych sheets generator')
    parser.add_argument('competition', nargs=None, default=None, type=str,
                        help='Input competition name')
    parser.add_argument('--output', '-o', default='psych.html', type=str,
                        help='Path to output html')
    parser.add_argument('--list-competitors', '-l', default=False, action='store_true',
                        help='Just print list of competitors')
    args = parser.parse_args()

    # Read competition
    compinfo = read_compinfo(args.competition)
    compdata = read_compdata(args.competition)

    # Read WCA results and generate psych
    latest_export = find_latest_export()
    wcaresults = read_wcaresults(compdata, latest_export)
    psych = generate_psych(wcaresults)

    if args.list_competitors:
        for competitor in compdata['competitors']:
            print competitor, compdata['competitorsname'][competitor]

    else:
        # Generate html
        env = Environment(loader=FileSystemLoader('./', encoding='utf8'))
        tpl = env.get_template(PSYCH_TEMPLATE)
        attrs = {'events_name': cubing.EVENTS_NAME, 'database_version': latest_export.split('.')[0]}
        html = tpl.render({'attrs': attrs, 'compinfo': compinfo, 'compdata': compdata, 'psych': psych})
        with open(args.output, 'w') as f:
            f.write(html.encode('utf-8'))
        print 'Complete writing to %s' % (args.output)
