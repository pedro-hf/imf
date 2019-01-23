import requests

# country: US, indicator: FILR_PA, start_date: 1950, end_date: 2016


def get_imf_data(country, indicator, start_date, end_date):
    """
    Function that queries the IMF's API to obtain the data to plot.
    :param country: string, ISO 2 code for the country to query
    :param indicator: string, Code for the IMF indicator
    :param start_date: string, first year to extract data from
    :param end_date: string, last year to extract data from.
    :return: json file with queried data
    """
    url = 'http://dataservices.imf.org/REST/SDMX_JSON.svc/CompactData/IFS/' \
          'Q.{}.{}.?startPeriod={}&endPeriod={}'.format(country, indicator, start_date, end_date)
    r = requests.get(url)
    d = r.json()
    data_json = d['CompactData']['DataSet']['Series']['Obs']
    return data_json
