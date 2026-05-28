from binance.client import Client
import pandas as pd
import ta
import time
import requests
import feedparser
from textblob import TextBlob
from ta.trend import MACD
from ta.momentum import RSIIndicator
from ta.volatility import BollingerBands
from ta.trend import EMAIndicator

# بيانات بوت التليجرام
TOKEN = "8108797876:AAGH62lPHmDbuLLapr_XluciZlD5hCCZhiE"
CHAT_ID = "662991988"

# تشغيل Binance

client = Client()

# العملات

symbols = [
"BTCUSDT",
"ETHUSDT",
"BNBUSDT",
"SOLUSDT",
"XRPUSDT"
]

# منع تكرار الإشارات

last_signals = {}

# تحليل الأخبار بالذكاء الاصطناعي

def analyze_news():
    return "NEUTRAL"
```
try:

    feed = feedparser.parse(
        "https://cointelegraph.com/rss"
    )

    news_text = ""

    for entry in feed.entries[:5]:
        news_text += entry.title + " "

    analysis = TextBlob(news_text)

    sentiment = analysis.sentiment.polarity

    if sentiment > 0:
        return "BULLISH"

    elif sentiment < 0:
        return "BEARISH"

    else:
        return "NEUTRAL"

except:
    return "UNKNOWN"
```

# تشغيل دائم

while True:

```
try:

    market_sentiment = get_market_sentiment()

    for symbol in symbols:

        # جلب البيانات
        klines = client.get_klines(
            symbol=symbol,
            interval=Client.KLINE_INTERVAL_5MINUTE,
            limit=200
        )

        # تحويل البيانات
        df = pd.DataFrame(klines)

        # الأسعار
        df["close"] = df[4].astype(float)
        df["high"] = df[2].astype(float)
        df["low"] = df[3].astype(float)

        # RSI
        rsi = RSIIndicator(df["close"])
        df["RSI"] = rsi.rsi()

        # EMA
        ema20 = EMAIndicator(
            df["close"],
            window=20
        ).ema_indicator().iloc[-1]

        ema50 = EMAIndicator(
            df["close"],
            window=50
        ).ema_indicator().iloc[-1]

        # MACD
        macd = MACD(df["close"])

        macd_value = macd.macd().iloc[-1]
        macd_signal = macd.macd_signal().iloc[-1]

        # Bollinger Bands
        bb = BollingerBands(df["close"])

        upper_band = bb.bollinger_hband().iloc[-1]
        lower_band = bb.bollinger_lband().iloc[-1]

        # السعر الحالي
        current_price = df["close"].iloc[-1]

        # RSI الحالي
        last_rsi = df["RSI"].iloc[-1]

        # قوة الصفقة
        signal_strength = round(
            abs(macd_value - macd_signal) * 100,
            2
        )

        # وقف خسارة
        stop_loss = round(
            current_price * 0.98,
            2
        )

        # جني أرباح
        take_profit = round(
            current_price * 1.04,
            2
        )

        print("======================")
        print("COIN:", symbol)
        print("PRICE:", current_price)
        print("RSI:", last_rsi)
        print("MARKET:", market_sentiment)

        # BUY SIGNAL
        if (
            ema20 > ema50
            and macd_value > macd_signal
            and last_rsi < 70
            and market_sentiment != "BEARISH"
        ):

            signal = "BUY"

            if last_signals.get(symbol) != signal:

                requests.post(
                    f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                    data={
                        "chat_id": CHAT_ID,
                        "text":
                        f"🚀 BUY SIGNAL 🚀\n\n"
                        f"COIN: {symbol}\n"
                        f"PRICE: {current_price}\n"
                        f"RSI: {round(last_rsi,2)}\n"
                        f"AI MARKET: {market_sentiment}\n"
                        f"STRENGTH: {signal_strength}%\n"
                        f"TAKE PROFIT: {take_profit}\n"
                        f"STOP LOSS: {stop_loss}"
                    }
                )

                last_signals[symbol] = signal

        # SELL SIGNAL
        elif (
            ema20 < ema50
            and macd_value < macd_signal
            and market_sentiment != "BULLISH"
        ):

            signal = "SELL"

            if last_signals.get(symbol) != signal:

                requests.post(
                    f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                    data={
                        "chat_id": CHAT_ID,
                        "text":
                        f"🔻 SELL SIGNAL 🔻\n\n"
                        f"COIN: {symbol}\n"
                        f"PRICE: {current_price}\n"
                        f"RSI: {round(last_rsi,2)}\n"
                        f"AI MARKET: {market_sentiment}\n"
                        f"STRENGTH: {signal_strength}%"
                    }
                )

                last_signals[symbol] = signal

        else:

            print(symbol, "NO SIGNAL")

    # انتظار 5 دقائق
    time.sleep(300)

except Exception as e:

    print("ERROR:", e)

    time.sleep(60)
```
