from common.database import Database
from common.environment import Env

ticker_field_dict = {'baseVolume':    'REAL', 
                     'high24hr':      'REAL', 
                     'highestBid':    'REAL', 
                     'last':          'REAL', 
                     'low24hr':       'REAL', 
                     'lowestAsk':     'REAL', 
                     'percentChange': 'REAL', 
                     'quoteVolume':   'REAL'}


if __name__ == '__main__':
       env = Env()
       db = Database(env)
       for pair in env.config.common.trade_pairs:
           ticker_field_dict['time'] = "TimeStamp  NOT NULL  DEFAULT (datetime('now','localtime'))"
           db.createTable(pair, ticker_field_dict)
