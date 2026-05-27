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

            # إشارة شراء
            if ema20 > ema50 and macd_value > macd_signal:

                requests.post(
                    f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                    data={
                        "chat_id": CHAT_ID,
                        "text": f"BUY SIGNAL 🚀\n{symbol}\nPrice: {current_price}"
                    }
                )

            # إشارة بيع
            elif ema20 < ema50 and macd_value < macd_signal:

                requests.post(
                    f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                    data={
                        "chat_id": CHAT_ID,
                        "text": f"SELL SIGNAL 🔻\n{symbol}\nPrice: {current_price}"
                    }
                )

            else:
                print("NO SIGNAL")

        # انتظار دقيقة
        time.sleep(60)

    except Exception as e:

        print("ERROR:", e)

        time.sleep(30)