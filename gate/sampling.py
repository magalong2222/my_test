from common.environment import Env
from common.db_access import Database
from gate.gate_api import GateIO
import time


if __name__ == '__main__':
    env = Env()
    db = Database(env)
    gate_query = GateIO(env.config.gate.api_query_url,
                           env.config.gate.api_key,
                           env.config.gate.scret_key)
    while(True):
        for pair in env.config.common.trade_pairs:
            price_dict = gate_query.ticker(pair)
            if price_dict['result'] == 'true':
                price_dict.pop('result')
                db.insert(pair, price_dict)
            else:
                print('Error: Fetch real time price failed.')
        time.sleep(10)
    #print(db.query('eos_usdt', {'*':''}))
    #print(db.query('btm_usdt', {'*':''}))
