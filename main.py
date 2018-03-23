from common.environment import Env
from gate.gate_api import GateIO
from common.db_access import Database
import pdb

if __name__ == '__main__':
       env = Env()
       #gate_query = GateIO(env.config.gate.api_query_url,
       #                    env.config.gate.api_key,
       #                    env.config.gate.scret_key)
       #  Market Info
       #my_pair_list = []
       #pairs = gate_query.pairs()
       #for pair in pairs:
       #    if pair.find('usdt') != -1:
       #        my_pair_list.append(pair)
       #print(my_pair_list)
       #pdb.set_trace()
       db = Database(env)
       #db.createTable('test',{'AAA':'text','BBB':'text'})
       #db.insert('test', {'AAA':'111', 'BBB':'222'})
       #result = db.query('eos_usdt', {'*':''})
       #result = db.execute('select count(rowid) from eos_usdt')
       result = db.execute('select time,last from eos_usdt')
       print(result.fetchall())
       

