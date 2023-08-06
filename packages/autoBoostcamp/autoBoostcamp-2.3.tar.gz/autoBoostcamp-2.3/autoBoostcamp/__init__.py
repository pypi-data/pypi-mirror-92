__all__ = ["backend"]

from .backend import doHi, doBye, quick_start
import datetime

def do():
    now = datetime.datetime.now()
    now_hm = now.hour + 0.01 * now.minute
    if 9.40 <= now_hm <= 10.5:  # 9시 40분 ~ 10시5분
        doHi()
        print(f"autoBoostcamp doHi run")
    elif now_hm >= 19:  # 19시 ~
        doBye()
        print(f"autoBoostcamp doBye run")