from binance.client import Client
import pandas as pd
import ta
import time
import requests

# بيانات بوت التليجرام
TOKEN = "8108797876:AAGH62lPHmDbuLLapr_XluciZlD5hCCZhiE"
CHAT_ID = "662991988"

# تشغيل البايننس
client = Client(testnet=True)

# منع تكرار الإشارات
last_signal = ""

while True:

    try:

        # جلب بيانات BTC
        klines = client.get_klines(
            symbol="BTCUSDT",
            interval=Client.KLINE_INTERVAL_1MINUTE,
            limit=100
        )

        # تحويل البيانات
        df = pd.DataFrame(klines)

        # سعر الإغلاق
        df['close'] = df[4].astype(float)

        # حساب RSI
        rsi = ta.momentum.RSIIndicator(df['close'])

        df['RSI'] = rsi.rsi()

        # آخر سعر و RSI
        current_price = df['close'].iloc[-1]

        last_rsi = df['RSI'].iloc[-1]

        print("====================")
        print("Current Price:", current_price)
        print("Current RSI:", last_rsi)

        # إشارة شراء
        if last_rsi < 30 and last_signal != "BUY":

            last_signal = "BUY"

            print("BUY SIGNAL")

            requests.get(
                f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                params={
                    "chat_id": CHAT_ID,
                    "text": f"BUY SIGNAL BTCUSDT\nPrice: {current_price}"
                }
            )

        # إشارة بيع
        elif last_rsi > 70 and last_signal != "SELL":

            last_signal = "SELL"

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

    except Exception as e:

        print("ERROR:", e)

        time.sleep(30)