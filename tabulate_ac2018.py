#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cubing

import argparse
from bs4 import BeautifulSoup
import os
import re
import urllib2
import zipfile


def download_compdata_ac2018():
    """ Downloads registered data from AC2018 """
    html = urllib2.urlopen('https://cubing-tw.net/event/2018AsianChampionship/competitors').read()
    html = html.replace('<tbody>', '<tbody><tr>').replace('</tr>\n', '</tr><tr>')
    soup = BeautifulSoup(html, 'html.parser')
    html_table = str(soup.find('table'))
    # html is incomplete
    soup_table = BeautifulSoup(html_table, 'html.parser')
    soup_tr = soup_table.find_all('tr')

    # For WCA ID pattern match
    wcaid_pattern = r"[0-9]{4}[A-Z]{4}[0-9]{2}"
    wcaid_repatter = re.compile(wcaid_pattern)

    #competitors, competitorsname, competitorscountry, entries = [], {}, {}, {}
    competitors = []
    n = 1
    for tr in soup_tr:

        soup_td = tr.find_all('td')
        # 'td_data' is a list which contains entry list's raw text data.
        #   td_data = [ #, lastname, firstname, wca id, location, event ...... ]
        td_data = []
        for td in soup_td:
            td_data.append(td.get_text())

        # If length is 24, it is competitor's data
        if len(td_data) == 24:
            data = {}
            wca_id = ''
            name = ''
            if wcaid_repatter.match(td_data[2]):
                wca_id = td_data[2]
            else:
                wca_id = '0' #wca_id = 'N_%03d' % n
                n = n + 1
                name = td_data[1]
            data['wca_id'] = wca_id
            data['name'] = name
            if 'Female' in td_data[4]:
                data['gender'] = 'f'
            else:
                data['gender'] = 'm'
            entries = []
            ei = 0
            for attend in td_data[5:23]:
                entries.append((attend != '-'))
                ei = ei + 1
            data['entries'] = entries
            competitors.append(data)

    return competitors


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Tabulate AC2018')
    parser.add_argument('--output', '-o', default='ac-2018.csv', type=str,
                        help='Path to output CSV')
    args = parser.parse_args()

    # Read competition
    competitors = download_compdata_ac2018()

    with open(args.output, 'w') as f:
        f.write('ID,333,333female,222,444,555,666,777,333bf,333fm,333oh,333ft,clock,minx,pyram,skewb,sq1,444bf,555bf,333mbf,name (competitor w/o WCAID)\n')
        for c in competitors:
            f.write(c['wca_id'] + ',')
            is_333 = True
            for e in c['entries']:
                if e:
                    f.write('X,')
                else:
                    f.write(',')
                if is_333:
                    if e and (c['gender'] == 'f'):
                        f.write('X,')
                    else:
                        f.write(',')
                    is_333 = False
            f.write(c['name'].encode('utf-8') + '\n')
