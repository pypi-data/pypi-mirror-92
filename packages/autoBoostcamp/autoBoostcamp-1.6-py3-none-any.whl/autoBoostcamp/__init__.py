from .autoBoostcampBackend import doHi, doBye
import datetime

def do():
    now = datetime.datetime.now()
    now_hm = now.hour + 0.01 * now.minute
    if 9.30 <= now_hm <= 10:  # 9시 30분 ~ 10시
        doHi()
        print(f"autoBoostcamp doHi run")
    elif now_hm >= 19:  # 19시 ~
        doBye()
        print(f"autoBoostcamp doBye run")

if __name__ == "__main__":
    do()