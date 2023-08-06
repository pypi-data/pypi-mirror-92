import argparse
from .autoBoostcampBackend import doHi, doBye

parser = argparse.ArgumentParser()
parser.add_argument("--mode", default='client') # pydev interactive console에서 사용 시 필요
parser.add_argument("--port", default=52162) # pydev interactive console에서 사용 시 필요
parser.add_argument('--isHi', type=eval, default=False, help='True at hi, False at bye')
args = parser.parse_args()

def do():
    print(f"autoBoostcamp Run with isHi = {args.isHi}")
    isHi = args.isHi
    if isHi == True:
        doHi()
    else:
        doBye()