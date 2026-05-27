from binance.client import Client
import pandas as pd
import ta
import time
import requests


# بيانات بوت التليجرام
TOKEN = "8108797876:AAGH62lPHmDbuLLapr_XluciZlD5hCCZhiE"
CHAT_ID = "662991988"

# تشغيل البايننس تيست نت
client = Client()

# العملات
symbols = [
    "BTCUSDT",
    "ETHUSDT",
    "BNBUSDT",
    "SOLUSDT",
    "XRPUSDT"
]

# حفظ آخر إشارة
last_signals = {}

while True:

    try:

        for symbol in symbols:

            print(f"\n===== {symbol} =====")

            # جلب البيانات
            klines = client.get_klines(
                symbol=symbol,
                interval=Client.KLINE_INTERVAL_1MINUTE,
                limit=100
            )

            # تحويل البيانات
            df = pd.DataFrame(klines)

            # سعر الإغلاق
            df["close"] = df[4].astype(float)

            # RSI
            rsi = ta.momentum.RSIIndicator(df["close"])
            df["RSI"] = rsi.rsi()

            # EMA
            ema20 = df["close"].ewm(span=20).mean().iloc[-1]
            ema50 = df["close"].ewm(span=50).mean().iloc[-1]

            # MACD
            macd = ta.trend.MACD(df["close"])
            macd_value = macd.macd().iloc[-1]
            macd_signal = macd.macd_signal().iloc[-1]

            # آخر سعر
            current_price = df["close"].iloc[-1]

            print("Price:", current_price)
            print("EMA20:", ema20)
            print("EMA50:", ema50)
            print("MACD:", macd_value)
            print("MACD SIGNAL:", macd_signal)

            # شراء
            if ema20 > ema50 and macd_value > macd_signal:

                if last_signals.get(symbol) != "BUY":

                    last_signals[symbol] = "BUY"

                    message = f"""
🚀 BUY SIGNAL
Coin: {symbol}

Price: {current_price}
EMA20 > EMA50
MACD Positive
"""

                    requests.post(
                        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                        data={
                            "chat_id": CHAT_ID,
                            "text": message
                        }
                    )

                    print("BUY SENT")

            # بيع
            elif ema20 < ema50 and macd_value < macd_signal:

                if last_signals.get(symbol) != "SELL":

                    last_signals[symbol] = "SELL"

                    message = f"""
🔻 SELL SIGNAL
Coin: {symbol}

Price: {current_price}
EMA20 < EMA50
MACD Negative
"""

                    requests.post(
                        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                        data={
                            "chat_id": CHAT_ID,
                            "text": message
                        }
                    )

                    print("SELL SENT")

            else:
                print("NO SIGNAL")

        # انتظار دقيقة
        time.sleep(60)

    except Exception as e:

        print("ERROR:", e)

        time.sleep(30)