import requests
import pandas as pd

class IMFClient:
    imf_url = 'http://dataservices.imf.org/REST/SDMX_JSON.svc/'

    def get_imf_data(self, country, indicator, start_date, end_date):
        """
        Function that queries the IMF's API to obtain the data to plot.
        :param country: string, ISO 2 code for the country to query
        :param indicator: string, Code for the IMF indicator
        :param start_date: string, first year to extract data from
        :param end_date: string, last year to extract data from.
        :return: json file with queried data
        """
        url = self.imf_url + 'CompactData/IFS/' \
                             'M.{}.{}.?startPeriod={}&endPeriod={}'.format(country, indicator, start_date, end_date)
        r = requests.get(url)
        d = r.json()
        data_json = d['CompactData']['DataSet']['Series']['Obs']
        return pd.DataFrame().from_dict(data_json)

    def get_dataflow_codes(self, d='IFS'):
        url = self.imf_url + '/DataStructure/' + d
        r = requests.get(url)
        d = r.json()
        codes = pd.DataFrame().from_dict(d['Structure']['CodeLists']['CodeList'][3]['Code'])
        codes['Description'] = codes.Description.apply(lambda dct: dct['#text'])
        codes.rename(columns={'@value': 'code'}, inplace=True)
        codes.set_index('code', inplace=True)
        return codes
