# region imports
from AlgorithmImports import *
# endregion

class WaveTrendOscillator(QCAlgorithm):

    def initialize(self):
        self.set_start_date(2020, 1, 1)
        self.set_end_date(2024, 1, 1)
        self.set_cash(100000)
        self.spy=self.add_equity("SPY", Resolution.DAILY).symbol
        self.channel_length=10
        self.avg_length = 21
        self.signal_length = 4
        self.no_of_history_days=self.avg_length*4
        self.set_warm_up(self.no_of_history_days)


    def on_data(self, data: Slice):
        self.wt_oscillator, self.wt_signal = self.WaveTrendOscillator(self.spy, self.channel_length, self.avg_length, self.signal_length)

        wt_value = self.wt_oscillator.iloc[-1]  # Get the last value
        wt_signal = self.wt_signal.iloc[-1]  # Get the last value
        if pd.isna(wt_value) or pd.isna(wt_signal):
            return

    # Log the current wt_value
        self.Log(f"WaveTrend Oscillator value: {wt_value}")
        if not self.portfolio.invested and wt_value<-50 and wt_value>wt_signal:
            self.set_holdings("SPY", 1)
        elif self.portfolio.invested and wt_value > 50 and wt_value < wt_signal:
            self.liquidate("SPY")

    
    def WaveTrendOscillator(self,symbol,channel_length,avg_length,signal_length):
        history=self.History(symbol,self.no_of_history_days,Resolution.DAILY)
        close=history["close"]
        high=history["high"]
        low=history["low"]

        hlc3=(high+low+close)/3
        self.Log(f"hlc3: {hlc3}")
        esa=hlc3.ewm(span=channel_length).mean()
        self.Log(f"esa: {esa}")
        deviation=abs(hlc3-esa).ewm(span=channel_length).mean()
        self.Log(f"deviation: {deviation}")
        ci=(hlc3-esa)/(0.015 * deviation)

        wt=ci.ewm(span=avg_length).mean()

        signal=wt.ewm(span=signal_length).mean()
        self.Log(f"wt: {wt}")
        self.Log(f"signal: {signal}")
        return wt, signal
