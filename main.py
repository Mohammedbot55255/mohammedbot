from binance.client import Client
import pandas as pd
import ta
import time
import requests
import yfinance as yf

# بيانات بوت التليجرام
TOKEN = "8108797876:AAGH62lPHmDbuLLapr_XluciZlD5hCCZhiE"
CHAT_ID = "662991988"

# تشغيل البايننس
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

            # جلب البيانات
            klines = client.get_klines(
                symbol=symbol,
                interval=Client.KLINE_INTERVAL_1MINUTE,
                limit=100
            )

            # تحويل البيانات
            df = pd.DataFrame(klines)

            # سعر الإغلاق
            df['close'] = df[4].astype(float)

            # RSI
            rsi = ta.momentum.RSIIndicator(df['close'])
            df['RSI'] = rsi.rsi()

            current_price = df['close'].iloc[-1]
            last_rsi = round(df['RSI'].iloc[-1], 2)

            # EMA
            ema20 = df["close"].ewm(span=20).mean().iloc[-1]
            ema50 = df["close"].ewm(span=50).mean().iloc[-1]

            # MACD
            macd = ta.trend.MACD(df["close"])
            macd_value = macd.macd().iloc[-1]
            macd_signal = macd.macd_signal().iloc[-1]

            # قوة الإشارة
            signal_strength = round(abs(macd_value - macd_signal), 2)

            print("====================")
            print("COIN:", symbol)
            print("PRICE:", current_price)
            print("RSI:", last_rsi)

            # شراء
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
                            f"RSI: {last_rsi}\n"
                            f"STRENGTH: {signal_strength}"
                        }
                    )

                    last_signals[symbol] = signal

            # بيع
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
                            f"RSI: {last_rsi}\n"
                            f"STRENGTH: {signal_strength}"
                        }
                    )

                    last_signals[symbol] = signal

            else:
                print(f"{symbol}: NO SIGNAL")

        time.sleep(60)

    except Exception as e:
        print("ERROR:", e)
        time.sleep(30)