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


    def get_code_list_name(self, code_list, df):
        if code_list == 'area':
            return 'CL_AREA_{}'.format(df)
        elif code_list == 'freq':
            return 'CL_FREQ'
        elif code_list == 'indicator':
            return 'CL_INDICATOR_{}'.format(df)
        else:
            print('The possible code lists are area, freq or indicator')
            return None


    def get_dataflow_codes(self, df='IFS', code_list = 'indicator'):
        """
        Methods that returns the indicator codes for a specific indicator.
        :param d: dataflow code
        :return:
        """
        url = self.imf_url + '/DataStructure/' + df
        r = requests.get(url)
        d = r.json()
        ds_struct = pd.DataFrame().from_dict(d['Structure']['CodeLists']['CodeList'])
        ds_struct.set_index('@id', inplace=True)

        code_list_name = self.get_code_list_name(code_list, df)
        codes = pd.DataFrame.from_dict(ds_struct.loc[code_list_name]['Code'])
        codes['Description'] = codes.Description.apply(lambda dct: dct['#text'])
        codes.rename(columns={'@value': 'code'}, inplace=True)
        return codes

    def get_dataflows(self):
        """Method that returns a pandas dataframe with the dataflows IDs and descriptions"""
        url = self.imf_url + 'Dataflow'
        r = requests.get(url)
        data = r.json()
        dataflows = pd.DataFrame.from_dict(data['Structure']['Dataflows']['Dataflow'])
        dataflows['Description'] = dataflows.Name.apply(lambda d: d['#text'])
        dataflows['dataflowID'] = dataflows.KeyFamilyRef.apply(lambda d: d['KeyFamilyID'])
        dataflows = dataflows[['Description', 'dataflowID']]
        return dataflows
