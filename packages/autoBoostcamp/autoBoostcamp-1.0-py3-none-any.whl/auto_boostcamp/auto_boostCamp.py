import argparse
import os
import sys
os.chdir(os.path.dirname(sys.argv[0]))
from auto_boostCamp_backend import doHi, doBye

parser = argparse.ArgumentParser()
parser.add_argument("--mode", default='client') # pydev interactive console에서 사용 시 필요
parser.add_argument("--port", default=52162) # pydev interactive console에서 사용 시 필요
parser.add_argument('--isHi', type=eval, default=False, help='True at hi, False at bye')
args = parser.parse_args()

if args.isHi == True:
    doHi()
else:
    doBye()