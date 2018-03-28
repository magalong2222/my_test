from common.environment import Env
from gate.gate_api import GateIO
from common.db_access import Database
import pdb
import matplotlib.pyplot as plt
from analysis.fitting import MovePloyFit

if __name__ == '__main__':
       env = Env()
       move_poly = MovePloyFit(env, 900, 10)
       move_poly.realtime()
#       move_poly.showData()
