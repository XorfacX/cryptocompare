import requests
import time
import datetime

## API
 # Price
URL_PRICE = 'https://min-api.cryptocompare.com/data/pricemulti?fsyms={}&tsyms={}&e={}&tryConversion={}&extraParams={}&sign={}'
URL_PRICE_MULTI = 'https://min-api.cryptocompare.com/data/pricemulti?fsyms={}&tsyms={}&e={}&tryConversion={}&extraParams={}&sign={}'
URL_PRICE_MULTI_FULL = 'https://min-api.cryptocompare.com/data/pricemultifull?fsyms={}&tsyms={}&e={}&tryConversion={}&extraParams={}&sign={}'

URL_AVG = 'https://min-api.cryptocompare.com/data/generateAvg?fsym={}&tsym={}&e={}&extraParams={}&sign={}'

 # Historical
URL_HIST_PRICE_TIMESTAMP = 'https://min-api.cryptocompare.com/data/pricehistorical?fsym={}&tsyms={}&ts={}&e={}&calculationType={}&tryConversion={}&extraParams={}&sign={}'

URL_HIST_PRICE_DAY = 'https://min-api.cryptocompare.com/data/histoday?fsym={}&tsym={}&e={}&aggregate={}&aggregatePredictableTimePeriods={}&limit={}&allData={}&toTs={}&tryConversion={}&extraParams={}&sign={}'
URL_HIST_PRICE_HOUR = 'https://min-api.cryptocompare.com/data/histohour?fsym={}&tsym={}&e={}&aggregate={}&aggregatePredictableTimePeriods={}&limit={}&toTs={}&tryConversion={}&extraParams={}&sign={}'
URL_HIST_PRICE_MINUTE = 'https://min-api.cryptocompare.com/data/histominute?fsym={}&tsym={}&e={}&aggregate={}&aggregatePredictableTimePeriods={}&limit={}&toTs={}&tryConversion={}&extraParams={}&sign={}'

 # General Info
URL_COIN_LIST = 'https://www.cryptocompare.com/api/data/coinlist/'

URL_EXCHANGES = 'https://www.cryptocompare.com/api/data/exchanges'

# FIELDS
PRICE = 'PRICE'
HIGH = 'HIGH24HOUR'
LOW = 'LOW24HOUR'
VOLUME = 'VOLUME24HOUR'
CHANGE = 'CHANGE24HOUR'
CHANGE_PERCENT = 'CHANGEPCT24HOUR'
MARKETCAP = 'MKTCAP'

# DEFAULTS
defCOIN = 'BTC' #NB: be careful that the BTC ticker is not always BTC (can be BTC, XBT, XBTUSD, ...)
defCURRENCY = 'EUR'
LIMIT = 2000
###############################################################################

def query_cryptocompare(url, errorCheck=True):
    try:
        response = requests.get(url).json()
    except Exception as e:
        print('Error getting coin information. %s' % str(e))
        return None
    if errorCheck and (response.get('Response') == 'Error'):
        print('[ERROR] %s' % response.get('Message'))
        return None
    return response

def format_parameter(parameter):
    if isinstance(parameter, list):
        return ','.join(parameter)
    else:
        return parameter

###############################################################################

def get_coin_list(format=False):
    response = query_cryptocompare(URL_COIN_LIST, False)['Data']
    if format:
        return list(response.keys())
    else:
        return response

#TODO: add option to filter json response according to a list of fields
#TODO check exchange name is in list
def get_price(coin=defCOIN, curr=defCURRENCY, exchange='CCCAGG', tryConversion=True, appName=' ', sign=False, full=False):
    if full:
        return query_cryptocompare( URL_PRICE_MULTI_FULL.format( format_parameter(coin), format_parameter(curr), format_parameter(exchange), int(tryConversion), appName, int(sign) ) )
    if isinstance(coin, list):
        return query_cryptocompare( URL_PRICE_MULTI.format( format_parameter(coin), format_parameter(curr), format_parameter(exchange), int(tryConversion), appName, int(sign) ) )
    else:
        return query_cryptocompare( URL_PRICE.format( coin, format_parameter(curr), format_parameter(exchange), int(tryConversion), appName, int(sign) ) )


def get_avg(coin=defCOIN, curr=defCURRENCY, exchange='CCCAGG', appName=' ', sign=False):
    response = query_cryptocompare( URL_AVG.format( coin, curr, format_parameter(exchange), appName, int(sign) ) )
    if response:
        return response['RAW']
        
#TODO check  calculationType is in ['Close', 'MidHighLow', 'VolFVolT']
def get_historical_price_ts(coin=defCOIN, curr=defCURRENCY, timestamp=time.time(), exchange='CCCAGG', calculationType='Close', tryConversion=True, appName=' ', sign=False):
    if isinstance(timestamp, datetime.datetime):
        timestamp = time.mktime(timestamp.timetuple())
    return query_cryptocompare( URL_HIST_PRICE_TIMESTAMP.format( coin, format_parameter(curr), int(timestamp), format_parameter(exchange), calculationType, int(tryConversion), appName, int(sign) ) )

#TODO check 1 <= agregate <= 30
#TODO check curr/coin are not arrays
def get_historical_price_day(coin=defCOIN, curr=defCURRENCY, exchange='CCCAGG', aggregate=1, aggregatePredictableTimePeriods=True, limit=LIMIT, allData=False, toTs=time.time(), tryConversion=True, appName=' ', sign=False):
    return query_cryptocompare( URL_HIST_PRICE_DAY.format( coin, format_parameter(curr), format_parameter(exchange), int(aggregate), int(aggregatePredictableTimePeriods), limit, int(allData), int(toTs), int(tryConversion), appName, int(sign) ) )

#TODO check 1 <= agregate <= 30
#TODO check curr/coin are not arrays
def get_historical_price_hour(coin=defCOIN, curr=defCURRENCY, exchange='CCCAGG', aggregate=1, aggregatePredictableTimePeriods=True, limit=LIMIT, toTs=time.time(), tryConversion=True, appName=' ', sign=False):
    return query_cryptocompare( URL_HIST_PRICE_HOUR.format( coin, format_parameter(curr), format_parameter(exchange), int(aggregate), int(aggregatePredictableTimePeriods), limit, int(toTs), int(tryConversion), appName, int(sign) ) )

#TODO check 1 <= agregate <= 30
#TODO check curr/coin are not arrays
def get_historical_price_minute(coin=defCOIN, curr=defCURRENCY, exchange='CCCAGG', aggregate=1, aggregatePredictableTimePeriods=True, limit=LIMIT, toTs=time.time(), tryConversion=True, appName=' ', sign=False):
    return query_cryptocompare( URL_HIST_PRICE_MINUTE.format( coin, format_parameter(curr), format_parameter(exchange), int(aggregate), int(aggregatePredictableTimePeriods), limit, int(toTs), int(tryConversion), appName, int(sign) ) )



def get_exchanges():
    response = query_cryptocompare(URL_EXCHANGES)
    if response:
        return response['Data']
