import requests
import pandas as pd


class IMFClient:
    """ Client designed to query the JSON REST API from the IMF """

    imf_url = 'http://dataservices.imf.org/REST/SDMX_JSON.svc/'

    def __repr__(self):
        answer = 'Connected to {}'.format(self.imf_url)
        return answer

    def __get_dataflow_codes(self, dataflow, code_list):
        """
        Method that returns the indicator codes for a specific indicator.
        :param dataflow: string, dataflow (e.g. IFS)
        :param code_list: string, name of the code list to extract values (e.g. CL_AREA_IFS)
        :return: codes: dataframe, dataframe containing the codes and description of codes.
        """
        url = self.imf_url + '/DataStructure/' + dataflow
        r = requests.get(url)
        d = r.json()
        ds_struct = pd.DataFrame().from_dict(d['Structure']['CodeLists']['CodeList'])
        ds_struct.set_index('@id', inplace=True)

        codes = pd.DataFrame.from_dict(ds_struct.loc[code_list]['Code'])
        codes['Description'] = codes.Description.apply(lambda dct: dct['#text'])
        codes.rename(columns={'@value': 'code', 'Description': 'value'}, inplace=True)
        return codes

    def get_data(self, dataflow, frequency, country, indicator, start_date, end_date):
        """
        Function that queries the IMF's API to obtain the data to plot.
        :param dataflow: string, dataflow to read flow
        :param frequency: string, String representing the frequency.
        :param country: string, ISO 2 code for the country to query
        :param indicator: string, Code for the IMF indicator
        :param start_date: string, first year to extract data from
        :param end_date: string, last year to extract data from.
        :return: json file with queried data
        """

        try:
            url = self.imf_url + 'CompactData/{}/' \
                                 '{}.{}.{}.?startPeriod={}&endPeriod={}'.format(dataflow, frequency, country,
                                                                                indicator, start_date, end_date)
            r = requests.get(url)
            if r.status_code == 200:
                d = r.json()
                data_json = d['CompactData']['DataSet']['Series']['Obs']
                data = pd.DataFrame().from_dict(data_json)
                data.rename({'@OBS_VALUE': 'value', '@TIME_PERIOD': 'time'}, axis=1, inplace=True)
                return data, 'data retrieved successfully'

            elif r.status_code == 500:
                return pd.DataFrame(columns=['value', 'time']), 'returned server error [500]'

        except KeyError:
            return pd.DataFrame(columns=['value', 'time']), 'data not available or in unexpected format'

        except TypeError:
            return pd.DataFrame(columns=['value', 'time']), 'data probably in unexpected format'

    def get_countries(self, dataflow):
        """Return a dataframe with the code value and the name of the areas, countries"""
        countries = self.__get_dataflow_codes(dataflow, 'CL_AREA_{}'.format(dataflow))
        return countries

    def get_indicators(self, dataflow):
        """Return a dataframe with the codes and descriptions of the indicators"""
        indicators = self.__get_dataflow_codes(dataflow, 'CL_INDICATOR_{}'.format(dataflow))
        return indicators

    def get_frequencies(self, dataflow):
        """Returns a dataframe with the availble frequencies for the dataflow"""
        frequencies = self.__get_dataflow_codes(dataflow, 'CL_FREQ'.format(dataflow))
        return frequencies

    def get_dataflows(self):
        """Method that returns a pandas dataframe with the dataflows IDs and descriptions"""
        url = self.imf_url + 'Dataflow'
        r = requests.get(url)
        data = r.json()
        dataflows = pd.DataFrame.from_dict(data['Structure']['Dataflows']['Dataflow'])
        dataflows['description'] = dataflows.Name.apply(lambda d: d['#text'])
        dataflows['dataflowID'] = dataflows.KeyFamilyRef.apply(lambda d: d['KeyFamilyID'])
        dataflows = dataflows[['description', 'dataflowID']]
        return dataflows
