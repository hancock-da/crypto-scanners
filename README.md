# crypto-scanners
*please note, these scanners are for educational purposes only and do not represent actual trading ideas*

1. crypto_snapshot.py pulls data for all USDT coin pairs from binance into a folder for scanning.

2. Scanners then *scan* through those datasets to find any cryptocurrency fulfilling certain conditions. If conditions are met, a notification will be sent to a discord channel.
> * kmeans_resistance_scanner.py finds support and resistance lines by using a kmeans clustering algorithm on prices. If, on the most recent day, a crypto closes above a resistance point, a notification will be sent.
> * three_line_strike_reversal_scanner.py will look for a three line strike candelstick pattern in the last few days. If the fast SMA is below the slow SMA, this pattern may indicate a bullish reversal.
> * breakout_scanner.py looks for periods of low volatility (default prices ranging within 5% for crypto) followed by a breakout and close above that level.
