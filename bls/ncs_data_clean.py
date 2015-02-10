import codecs
import locale
import os
import re
import sys

from bs4 import BeautifulSoup
import pymongo

# Wrap sys.stdout into a StreamWriter to allow writing unicode.
sys.stdout = codecs.getwriter(locale.getpreferredencoding())(sys.stdout)
sys.setrecursionlimit(2500)

db = pymongo.MongoClient().ncs


def process(clear=True):
    if clear:
        db.ebs.remove({})
    if db.ebs.count() > 0:
        return
    soup = None
    html_file = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            'ncs_data.html'))
    with open(html_file) as f:
        soup = BeautifulSoup(f)
    # clear the database
    tables = soup.find_all('table', class_='regular-data')
    for table in tables:
        pre = BeautifulSoup(
            re.sub(r'<strong>[^<]+</strong>', '', 
                   str(table.caption.pre)))
        desc = pre.prettify()
        desc = re.split(r'<[^>]+>', desc)
        desc = filter(len, map(unicode.strip, desc))
        (series_id, ownership, industry, estimate, datatype, occupation,
         subcell, provision) = desc
        rows = table.tbody.find_all('tr')
        year, period, value, se = '', '', '', ''
        for row in rows:
            year, period, value, se = [th.string.strip() for
                th in row.find_all(True, recursive=False)]
            if year == '2011':
                break
        if year != '2011':
            continue  # couldn't find data on 2011
        db.ebs.insert({
            'series_id': series_id,
            'ownership': ownership,
            'industry': industry,
            'estimate': estimate,
            'datatype': datatype,
            'occupation': occupation,
            'subcell': subcell,
            'provision': provision,
            'value': float(value),
            'se': se,
        })

if __name__ == '__main__':
    print 'Populating data base...'
    process()
    print '\n'.join(db.ebs.distinct('provision'))
