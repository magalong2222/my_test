import yaml
import os


class Common(object):
    def __init__(self):
        self.trade_pairs = ['btc_usdt']

    def setCfg(self, cfg_dict):
        if 'TRADE_PAIRS' in cfg_dict:
            self.trade_pairs = cfg_dict['TRADE_PAIRS']

class GateInterface(object):
    def __init__(self):
        self.api_query_url = 'data.gate.io'
        self.api_trade_url = 'api.gate.io'
        self.data_file = 'data/gate.db'
        self.api_key = ''
        self.scret_key = ''
        self.wallet_dict = ''

    def setCfg(self, cfg_dict):
        if 'API_QUERY_URL' in cfg_dict:
            self.api_query_url = cfg_dict['API_QUERY_URL']
        if 'API_TRADE_URL' in cfg_dict:
            self.api_trade_url = cfg_dict['API_TRADE_URL']
        if 'DATA_FILE' in cfg_dict:
            self.data_file = cfg_dict['DATA_FILE']
        self.api_key = cfg_dict['API_KEY']
        self.scret_key = cfg_dict['SCRET_KEY']
        self.wallet_dict = cfg_dict['WALLET']

class Config(object):
    def __init__(self):
        self.gate_accout_list = []
        program_path = os.getenv('PYTHONPATH')
        cfg_file = os.path.join(program_path, 'config.yaml')
        with open(cfg_file, 'r') as fd:
            cfg_dict = yaml.load(fd)
        if 'COMMON' in cfg_dict:
            self.common = Common()
            self.common.setCfg(cfg_dict['COMMON'])
        if 'GATE.IO' in cfg_dict:
            self.gate = GateInterface()
            self.gate.setCfg(cfg_dict['GATE.IO'])
        
        pass

