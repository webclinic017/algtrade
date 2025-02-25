import pandas as pd
import numpy as np

class Indicators:
    def __init__(self, opens, lows, highs, closes):
        self.close = closes
        self.open = opens
        self.low = lows
        self.high = highs

    # Returns ATR values for set target point and stop loss
    def AverageTrueRange(self, number_range=14, ema=True):
        tr = np.amax(np.vstack(((self.high-self.low).to_numpy(), 
                    (abs(self.high-self.close)).to_numpy(), 
                    (abs(self.low-self.close)).to_numpy())).T, axis=1)
        return pd.Series(tr).rolling(number_range).mean().to_numpy()

    # Get RSI indicator for work with our logic
    def RSI(self, periods=14, ema=True):
        close_delta = self.close.diff()

        up = close_delta.clip(lower=0)
        down = -1 * close_delta.clip(upper=0)

        if ema==True:
            ma_up = up.ewm(com=periods-1, adjust=True, min_periods=periods).mean()
            ma_down = down.ewm(com=periods-1, adjust=True, min_periods=periods).mean()
        else:
            ma_up = up.rolling(window=periods, adjust=False).mean()
            ma_down = down.rolling(window=periods, adjust=False).mean()

        rsi = ma_up / ma_down
        rsi = 100 - (100/(1 + rsi))
        return rsi

    def Moving_Average(self, days=200):
        moving_averages = self.close.rolling(days).mean()
        return moving_averages

    def Bollian_Band(self, std=2, days=20):
        MA = self.close.rolling(window=days).mean()
        STD = self.close.rolling(window=days).std()
        Upper = MA + std*STD
        Lower = MA - std*STD
        return Upper, Lower

    # Get Stochastic Gradient Descent
    def stocastic(self, df ,k_period=14, d_period=3, col="BTC"):
        df['n_high'] = self.high.rolling(k_period).max()
        df['n_low'] = self.low.rolling(k_period).min()
        df['%K'] = (self.close-df['n_low'])*100/(df['n_high']-df['n_low'])
        Dstoc = df['%K'].rolling(d_period).mean()
        Kstoc = df['%K']
        return Kstoc, Dstoc

    # Get MACD Indicator for testing other algoritm
    def MACD(self, price, slow, fast, smooth):
        exp1 = price.ewm(span=fast, adjust=False).mean()
        exp2 = price.ewm(span=slow, adjust=False).mean()
        macd = pd.DataFrame(exp1 - exp2).rename(columns={'close':'macd'})
        signal = pd.DataFrame(macd.ewm(span=smooth, adjust=False).mean()).rename(
                                                            columns={'macd':'signal'})
        hist = pd.DataFrame(macd['macd']-signal['signal']).rename(columns={0:'hist'})
        frames =  [macd, signal, hist]
        df = pd.concat(frames, join='inner', axis=1)
        return df
