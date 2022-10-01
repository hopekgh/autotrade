import time
import pyupbit
import datetime
import requests
from ta import trend
access = "HeHh5v7uflluT2ChATZ0BgcIqo3IAGPSHJgcBzMT"
secret = "07uTQ7VxPXmspfATpV7YoEPyYkchHinTYMH4IzeB"
myToken = ""
time_interval = "minute240"
tick= "KRW-EOS"
def post_message(token, channel, text):
    """슬랙 메시지 전송"""
    response = requests.post("https://slack.com/api/chat.postMessage",
        headers={"Authorization": "Bearer "+token},
        data={"channel": channel,"text": text}
    )

def get_target_price(ticker, k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval=time_interval, count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price

def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval=time_interval, count=1)
    start_time = df.index[0]
    return start_time

def get_ma60(ticker):
    """15일 이동 평균선 조회"""
    df = pyupbit.get_ohlcv(ticker, interval=time_interval, count=60)
    ma60 = trend.EMAIndicator(df["close"],60).ema_indicator().iloc[-1]
    return ma60

def get_ma180(ticker):
    """15일 이동 평균선 조회"""
    df = pyupbit.get_ohlcv(ticker, interval=time_interval, count=180)
    ma180 = trend.EMAIndicator(df["close"],180).ema_indicator().iloc[-1]
    return ma180

def get_balance(ticker):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
      print(b)
      if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0

def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(ticker=ticker)["orderbook_units"][0]["ask_price"]

# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")
# 시작 메세지 슬랙 전송
post_message(myToken,"#stock-auto", "autotrade start")

while True:
    try:
        now = datetime.datetime.now()
        start_time = get_start_time(tick)
        end_time = start_time + datetime.timedelta(days=1)

        if start_time < now < end_time - datetime.timedelta(seconds=10):
            target_price = get_target_price(tick, 0.5)
            ma60 = get_ma60(tick)
            ma180 = get_ma180(tick)
            current_price = get_current_price(tick)
            if target_price < current_price and ma180 < ma60:
                krw = get_balance("KRW")
                if krw > 5000:
                    buy_result = upbit.buy_market_order(tick, krw*0.9995)
                    post_message(myToken,"#crypto", "BTC buy : " +str(buy_result))
        else:
            btc = get_balance("EOS")
            if btc > 0.00008:
                sell_result = upbit.sell_market_order(tick, btc*0.9995)
                post_message(myToken,"#crypto", tick, " buy : " +str(sell_result))
        time.sleep(1)
    except Exception as e:
        print(e)
        post_message(myToken,"#stock-auto", e)
        time.sleep(1)
