import pandas as pd
import ta
import time
import requests
import yfinance as yf

# بيانات بوت التليجرام
TOKEN = "8108797876:AAGH62lPHmDbuLLapr_XluciZlD5hCCZhiE"
CHAT_ID = "662991988"

# العملات
symbols = [
    "BTC-USD",
    "ETH-USD",
    "BNB-USD"
]
last_signals = {}

while True:

    try:

        for symbol in symbols:

            # جلب البيانات
            data = yf.download(
                symbol,
                period="1d",
                interval="1m"
            )

            df = pd.DataFrame(data)

            # سعر الإغلاق
            df['close'] = df['Close']

            # RSI
            rsi = ta.momentum.RSIIndicator(df['close'])

            df['RSI'] = rsi.rsi()

            # EMA
            ema20 = df['close'].ewm(span=20).mean().iloc[-1]
            ema50 = df['close'].ewm(span=50).mean().iloc[-1]

            # MACD
            macd = ta.trend.MACD(df['close'])

            macd_value = macd.macd().iloc[-1]
            macd_signal = macd.macd_signal().iloc[-1]

            # السعر الحالي
            current_price = df['close'].iloc[-1]

            print(symbol)
            print("PRICE:", current_price)

# حساب قوة الإشارة
signal_strength = round(abs(macd_value - macd_signal), 2)

# إشارة شراء
if ema20 > ema50 and macd_value > macd_signal:

    signal = "BUY"

    if last_signals.get(symbol) != signal:

        requests.post(
            f"https://api.telegram.org/bot{TOKEN}/sendMessage",
            data={
                "chat_id": CHAT_ID,
                "text":
                f"🚀 BUY SIGNAL\n\n"
                f"COIN: {symbol}\n"
                f"PRICE: {current_price}\n"
                f"RSI: {round(df['RSI'].iloc[-1],2)}\n"
                f"STRENGTH: {signal_strength}"
            }
        )

        last_signals[symbol] = signal

# إشارة بيع
elif ema20 < ema50 and macd_value < macd_signal:

    signal = "SELL"

    if last_signals.get(symbol) != signal:

        requests.post(
            f"https://api.telegram.org/bot{TOKEN}/sendMessage",
            data={
                "chat_id": CHAT_ID,
                "text":
                f"🔻 SELL SIGNAL\n\n"
                f"COIN: {symbol}\n"
                f"PRICE: {current_price}\n"
                f"RSI: {round(df['RSI'].iloc[-1],2)}\n"
                f"STRENGTH: {signal_strength}"
            }
        )

        last_signals[symbol] = signal

else:
    print("NO SIGNAL")
    
        # انتظار دقيقة
        time.sleep(60)

    except Exception as e:

        print("ERROR:", e)

        time.sleep(30)