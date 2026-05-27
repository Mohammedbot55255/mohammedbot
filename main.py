from binance.client import Client
import pandas as pd
import ta
import time
import requests

# بيانات بوت التليجرام
TOKEN = "8108797876:AAGH62lPHmDbuLLapr_XluciZlD5hCCZhiE"
CHAT_ID = "662991988"

# تشغيل البايننس
client = Client(API_KEY, API_SECRET, testnet=True)

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

# حساب المؤشرات
ema20 = df["close"].ewm(span=20).mean().iloc[-1]
ema50 = df["close"].ewm(span=50).mean().iloc[-1]

macd = ta.trend.MACD(df["close"])
macd_value = macd.macd().iloc[-1]
macd_signal = macd.macd_signal().iloc[-1]

# طباعة المؤشرات
print("EMA20:", ema20)
print("EMA50:", ema50)
print("MACD:", macd_value)
print("MACD SIGNAL:", macd_signal)

# اشارة شراء
if ema20 > ema50 and macd_value > macd_signal:

    requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        data={
            "chat_id": CHAT_ID,
            "text": f"BUY SIGNAL BTCUSDT\nPrice: {current_price}"
        }
    )

# اشارة بيع
elif ema20 < ema50 and macd_value < macd_signal:

    requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        data={
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