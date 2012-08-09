#!/usr/bin/env python

from glob import glob
import codecs
from lxml import etree
from tableparser import tableparser

def find(v, f):
    try:
        return [i for i, vi in enumerate(v) if f(vi)][0]
    except:
        return None

def htmlbase(url):
    return url.split('/')[-1].replace('.html','')

def main():
    athletes = glob('www.sports-reference.com/olympics/athletes/??/*.html')

    records = codecs.open('records.tsv','w', encoding='utf-8')
    for athlete in athletes:
        html = open(athlete,'r')
        tree = etree.parse(html, etree.HTMLParser())
        html.close()
        
        tables = tree.xpath('//table[starts-with(@id,"results_")]')

        for table in tables:
            tp = tableparser(table)
            header = list(tp.header())

            cols = {'games': find(header, lambda x: x == 'Games'),
                    'age': find(header, lambda x: x == 'Age'),
                    'phase': find(header, lambda x: x == 'Phase'),
                    'rank': find(header, lambda x: x == 'Rank'),
                    'misc': find(header, lambda x: x == 'None'),
                    'time': find(header, lambda x: x == 'T' or x == 'T(A)'),
                    'distance': find(header, lambda x: x == 'D')
                    }

            try:
                tp.col_map[cols['games']] = tp.hypertext_map()
                tp.col_map[cols['phase']] = tp.hypertext_map()
            except:
                pass

            for row in tp.rows():

                year = str(row[cols['games']]).split(' ')[0]
                age = row[cols['age']]
                phase = row[cols['phase']]

                try:
                    rank = row[cols['rank']]
                except:
                    rank = ''

                try:
                    misc = row[cols['misc']]
                except TypeError:
                    misc = ''

                try:
                    time = row[cols['time']]
                except TypeError:
                    time = ''

                try:
                    distance = row[cols['distance']]
                except TypeError:
                    distance = ''

                records.write( "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (year, htmlbase(athlete), age, phase, htmlbase(phase.href), rank, misc, time, distance))

    return 0


if __name__=='__main__':
    main()
