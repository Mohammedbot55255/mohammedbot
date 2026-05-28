from binance.client import Client
import pandas as pd
import ta
import time
import requests
import feedparser
from textblob import TextBlob

# بيانات التليجرام

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

# تحليل الأخبار

def analyze_news():


try:
     feed = feedparser.parse(
        "https://cointelegraph.com/rss"
    )

    news_text = ""

    for entry in feed.entries[:5]:

        news_text += entry.title + " "

    analysis = TextBlob(news_text)

    polarity = analysis.sentiment.polarity

    if polarity > 0:

        return "POSITIVE"

    elif polarity < 0:

        return "NEGATIVE"

    else:

        return "NEUTRAL"

except:

    return "NEUTRAL"


# تشغيل البوت

while True:


try:

    news_sentiment = analyze_news()

    print(f"NEWS: {news_sentiment}")

    for symbol in symbols:

        print(f"تحليل {symbol}")

        klines = client.get_klines(
            symbol=symbol,
            interval=Client.KLINE_INTERVAL_15MINUTE,
            limit=100
        )

        df = pd.DataFrame(klines)

        close = df[4].astype(float)

        current_price = close.iloc[-1]

        ema20 = ta.trend.EMAIndicator(
            close,
            window=20
        ).ema_indicator().iloc[-1]

        ema50 = ta.trend.EMAIndicator(
            close,
            window=50
        ).ema_indicator().iloc[-1]

        macd = ta.trend.MACD(close)

        macd_value = macd.macd().iloc[-1]

        macd_signal = macd.macd_signal().iloc[-1]

        rsi = ta.momentum.RSIIndicator(
            close
        ).rsi().iloc[-1]

        signal_strength = round(
            abs(macd_value - macd_signal),
            2
        )

        signal = "NO SIGNAL"

        # شراء
        if (
            ema20 > ema50 and
            macd_value > macd_signal and
            rsi < 70 and
            news_sentiment != "NEGATIVE"
        ):

            signal = "BUY"

        # بيع
        elif (
            ema20 < ema50 and
            macd_value < macd_signal and
            rsi > 30 and
            news_sentiment != "POSITIVE"
        ):

            signal = "SELL"

        print(f"{symbol}: {signal}")

        if last_signals.get(symbol) != signal:

            message = f'''


🚨 SIGNAL ALERT 🚨

COIN: {symbol}

SIGNAL: {signal}

PRICE: {current_price}

RSI: {round(rsi,2)}

STRENGTH: {signal_strength}

NEWS: {news_sentiment}



             requests.post(
                f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                data={
                    "chat_id": CHAT_ID,
                    "text": message
                }
            )

            last_signals[symbol] = signal

    print("WAITING 5 MINUTES...")
    time.sleep(300)

except Exception as e:

    print("ERROR:", e)

    time.sleep(60)

