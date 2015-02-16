import json
import prettytable
import requests

"""
unused
"""


def fetch_series(series, startyear='2010', endyear='2014'):
    headers = {'Content-type': 'application/json'}
    data = json.dumps(
        {'seriesid': series, 'startyear': startyear, 'endyear': endyear})
    r = requests.post(
        'http://api.bls.gov/publicAPI/v2/timeseries/data/',
        data=data, headers=headers)

    print r.text
    json_data = json.loads(r.text)

    for series in json_data['Results']['series']:
        pt = prettytable.PrettyTable(
            ['series id','year','period','value','footnotes'])
        series_id = series['seriesID']
        for item in series['data']:
            year = item['year']
            period = item['period']
            value = item['value']
            footnotes = ''
            for footnote in item['footnotes']:
                if footnote:
                    footnotes += footnote['text'] + ', '
            if len(footnotes):
                footnotes = footnotes[:-2]
            pt.add_row([series_id,year,period,value,footnotes[0:-1]])
        with open(series_id + '.txt', 'w+') as output:
            output.write(pt.get_string())

if __name__ == '__main__':
    fetch_series(['NBU31461100000000022158'])
