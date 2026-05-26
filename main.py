from binance.client import Client
import pandas as pd
import ta
import time
import requests

# بيانات بوت التليجرام
TOKEN = "8108797876:AAGH62lPHmDbuLLapr_XluciZlD5hCCZhiE"
CHAT_ID = "662991988"

# تشغيل البايننس
client = Client()

while True:

    # جلب بيانات BTC
    klines = client.get_klines(
        symbol="BTCUSDT",
        interval=Client.KLINE_INTERVAL_1MINUTE,
        limit=100
    )

    # تحويل البيانات لجدول
    df = pd.DataFrame(klines)

    # سعر الإغلاق
    df['close'] = df[4].astype(float)

    # حساب RSI
    rsi = ta.momentum.RSIIndicator(df['close'])

    df['RSI'] = rsi.rsi()

    # آخر سعر و RSI
    current_price = df['close'].iloc[-1]

    last_rsi = df['RSI'].iloc[-1]

    # طباعة البيانات
    print("==============")

    print("Current Price:", current_price)

    print("Current RSI:", last_rsi)

    # إشارات التداول
    if last_rsi < 30:

        print("BUY SIGNAL")

        requests.get(
            f"https://api.telegram.org/bot{TOKEN}/sendMessage",
            params={
                "chat_id": CHAT_ID,
                "text": f"BUY SIGNAL BTCUSDT\nPrice: {current_price}"
            }
        )

    elif last_rsi > 70:

        print("SELL SIGNAL")

        requests.get(
            f"https://api.telegram.org/bot{TOKEN}/sendMessage",
            params={
                "chat_id": CHAT_ID,
                "text": f"SELL SIGNAL BTCUSDT\nPrice: {current_price}"
            }
        )

    else:

        print("NO SIGNAL")

    # انتظار دقيقة
    time.sleep(60)
