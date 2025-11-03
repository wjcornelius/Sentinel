"""
Extract Tickers from S&P 500 and Nasdaq 100 Lists
==================================================
Parses the user-provided lists and creates the full 600-stock universe.
"""

# S&P 500 tickers extracted from user data
sp500_tickers = [
    'NVDA', 'AAPL', 'MSFT', 'GOOG', 'GOOGL', 'AMZN', 'AVGO', 'META', 'TSLA', 'BRK.B',
    'JPM', 'WMT', 'LLY', 'ORCL', 'V', 'MA', 'XOM', 'PLTR', 'NFLX', 'JNJ',
    'AMD', 'COST', 'BAC', 'ABBV', 'HD', 'PG', 'GE', 'CVX', 'UNH', 'KO',
    'CSCO', 'IBM', 'WFC', 'CAT', 'MS', 'MU', 'AXP', 'CRM', 'GS', 'RTX',
    'TMUS', 'PM', 'APP', 'ABT', 'MRK', 'TMO', 'MCD', 'DIS', 'UBER', 'PEP',
    'ANET', 'LRCX', 'LIN', 'QCOM', 'NOW', 'INTC', 'ISRG', 'INTU', 'AMAT', 'C',
    'BX', 'BLK', 'T', 'SCHW', 'APH', 'NEE', 'VZ', 'BKNG', 'AMGN', 'KLAC',
    'GEV', 'TJX', 'ACN', 'BA', 'DHR', 'BSX', 'PANW', 'GILD', 'ETN', 'SPGI',
    'TXN', 'ADBE', 'PFE', 'COF', 'CRWD', 'SYK', 'LOW', 'UNP', 'HOOD', 'HON',
    'DE', 'WELL', 'PGR', 'PLD', 'CEG', 'MDT', 'ADI', 'LMT', 'COP', 'VRTX',
    'CB', 'DASH', 'DELL', 'KKR', 'ADP', 'HCA', 'SO', 'CMCSA', 'MCK', 'TT',
    'CVS', 'PH', 'DUK', 'CME', 'NKE', 'MO', 'BMY', 'GD', 'CDNS', 'SBUX',
    'MMM', 'NEM', 'COIN', 'MMC', 'MCO', 'SHW', 'SNPS', 'AMT', 'ICE', 'NOC',
    'EQIX', 'HWM', 'UPS', 'WM', 'ORLY', 'EMR', 'RCL', 'ABNB', 'GLW', 'BK',
    'JCI', 'MDLZ', 'TDG', 'CTAS', 'AON', 'TEL', 'USB', 'ECL', 'PNC', 'APO',
    'ITW', 'MAR', 'WMB', 'ELV', 'MSI', 'CSX', 'PWR', 'REGN', 'SPG', 'FTNT',
    'COR', 'CI', 'MNST', 'PYPL', 'GM', 'RSG', 'AEP', 'ADSK', 'AJG', 'WDAY',
    'ZTS', 'VST', 'NSC', 'CL', 'AZO', 'CMI', 'SRE', 'TRV', 'FDX', 'FCX',
    'HLT', 'DLR', 'MPC', 'KMI', 'EOG', 'TFC', 'AXON', 'AFL', 'DDOG', 'WBD',
    'URI', 'PSX', 'STX', 'LHX', 'APD', 'SLB', 'O', 'MET', 'NXPI', 'F',
    'VLO', 'ROST', 'PCAR', 'WDC', 'BDX', 'ALL', 'IDXX', 'D', 'CARR', 'EA',
    'PSA', 'NDAQ', 'EW', 'MPWR', 'ROP', 'XEL', 'BKR', 'TTWO', 'FAST', 'GWW',
    'EXC', 'AME', 'XYZ', 'CAH', 'CBRE', 'MSCI', 'DHI', 'AIG', 'ETR', 'KR',
    'OKE', 'TGT', 'PAYX', 'AMP', 'CMG', 'CTVA', 'CPRT', 'A', 'FANG', 'ROK',
    'GRMN', 'OXY', 'PEG', 'LVS', 'FICO', 'KMB', 'CCI', 'YUM', 'VMC', 'CCL',
    'TKO', 'DAL', 'MLM', 'KDP', 'IQV', 'EBAY', 'XYL', 'PRU', 'WEC', 'OTIS',
    'RMD', 'FI', 'SYY', 'CTSH', 'ED', 'PCG', 'WAB', 'VTR', 'EL', 'LYV',
    'HIG', 'NUE', 'HSY', 'DD', 'GEHC', 'CHTR', 'MCHP', 'HUM', 'EQT', 'NRG',
    'TRGP', 'FIS', 'STT', 'HPE', 'VICI', 'ACGL', 'LEN', 'KEYS', 'RJF', 'IBKR',
    'SMCI', 'VRSK', 'UAL', 'IRM', 'EME', 'IR', 'WTW', 'EXR', 'ODFL', 'KHC',
    'MTD', 'CSGP', 'ADM', 'TER', 'K', 'FOXA', 'TSCO', 'FSLR', 'MTB', 'DTE',
    'ROL', 'AEE', 'KVUE', 'ATO', 'FITB', 'ES', 'FOX', 'BRO', 'EXPE', 'WRB',
    'PPL', 'SYF', 'FE', 'HPQ', 'EFX', 'BR', 'CBOE', 'AWK', 'HUBB', 'CNP',
    'DOV', 'GIS', 'AVB', 'TDY', 'EXE', 'TTD', 'VLTO', 'LDOS', 'NTRS', 'HBAN',
    'CINF', 'PTC', 'WSM', 'JBL', 'NTAP', 'PHM', 'ULTA', 'STE', 'EQR', 'STZ',
    'STLD', 'TPR', 'DXCM', 'BIIB', 'HAL', 'CMS', 'TROW', 'VRSN', 'PODD', 'CFG',
    'PPG', 'DG', 'TPL', 'RF', 'EIX', 'CHD', 'LH', 'DRI', 'CDW', 'WAT',
    'L', 'NVR', 'DVN', 'SBAC', 'TYL', 'ON', 'IP', 'WST', 'LULU', 'NI',
    'DLTR', 'ZBH', 'KEY', 'DGX', 'RL', 'SW', 'TRMB', 'BG', 'GPN', 'IT',
    'J', 'PFG', 'CPAY', 'INCY', 'TSN', 'AMCR', 'CHRW', 'CTRA', 'GDDY', 'LII',
    'GPC', 'EVRG', 'APTV', 'PKG', 'SNA', 'PNR', 'CNC', 'INVH', 'BBY', 'MKC',
    'LNT', 'DOW', 'PSKY', 'ESS', 'WY', 'EXPD', 'HOLX', 'GEN', 'IFF', 'JBHT',
    'FTV', 'LUV', 'NWS', 'MAA', 'ERIE', 'LYB', 'NWSA', 'FFIV', 'OMC', 'ALLE',
    'TXT', 'KIM', 'COO', 'UHS', 'CLX', 'ZBRA', 'AVY', 'CF', 'DPZ', 'MAS',
    'EG', 'NDSN', 'BF.B', 'BLDR', 'IEX', 'BALL', 'DOC', 'HII', 'BXP', 'REG',
    'WYNN', 'UDR', 'VTRS', 'SOLV', 'DECK', 'HRL', 'BEN', 'ALB', 'SWKS', 'HST',
    'SJM', 'DAY', 'RVTY', 'JKHY', 'CPT', 'AKAM', 'HAS', 'AIZ', 'MRNA', 'PNW',
    'GL', 'IVZ', 'PAYC', 'SWK', 'NCLH', 'ARE', 'ALGN', 'FDS', 'POOL', 'AES',
    'GNRC', 'TECH', 'BAX', 'IPG', 'AOS', 'EPAM', 'CPB', 'CRL', 'MGM', 'MOS',
    'TAP', 'LW', 'DVA', 'FRT', 'CAG', 'LKQ', 'APA', 'MOH', 'MTCH', 'HSIC',
    'MHK', 'EMN'
]

# Nasdaq 100 tickers extracted from user data
nasdaq100_tickers = [
    'NVDA', 'AAPL', 'MSFT', 'AMZN', 'GOOGL', 'AVGO', 'GOOG', 'META', 'TSLA', 'PLTR',
    'NFLX', 'AMD', 'ASML', 'COST', 'CSCO', 'AZN', 'MU', 'TMUS', 'SHOP', 'APP',
    'PEP', 'LRCX', 'LIN', 'QCOM', 'PDD', 'INTC', 'ISRG', 'INTU', 'AMAT', 'ARM',
    'BKNG', 'AMGN', 'KLAC', 'PANW', 'GILD', 'TXN', 'ADBE', 'CRWD', 'HON', 'MELI',
    'CEG', 'ADI', 'VRTX', 'DASH', 'ADP', 'CMCSA', 'CDNS', 'SBUX', 'SNPS', 'MRVL',
    'ORLY', 'ABNB', 'MSTR', 'MDLZ', 'CTAS', 'MAR', 'TRI', 'REGN', 'CSX', 'FTNT',
    'MNST', 'PYPL', 'AEP', 'ADSK', 'WDAY', 'AXON', 'DDOG', 'WBD', 'NXPI', 'ZS',
    'ROST', 'PCAR', 'IDXX', 'EA', 'ROP', 'XEL', 'BKR', 'TTWO', 'FAST', 'EXC',
    'TEAM', 'PAYX', 'CPRT', 'FANG', 'CCEP', 'KDP', 'CTSH', 'GEHC', 'MCHP', 'CHTR',
    'VRSK', 'ODFL', 'KHC', 'CSGP', 'TTD', 'DXCM', 'BIIB', 'CDW', 'ON', 'LULU',
    'GFS'
]

# Combine and get unique tickers
all_tickers = sorted(set(sp500_tickers + nasdaq100_tickers))

print("=" * 70)
print("TICKER UNIVERSE EXTRACTION")
print("=" * 70)
print(f"\nS&P 500 tickers: {len(sp500_tickers)}")
print(f"Nasdaq 100 tickers: {len(nasdaq100_tickers)}")
print(f"Overlap: {len(sp500_tickers) + len(nasdaq100_tickers) - len(all_tickers)}")
print(f"TOTAL UNIQUE: {len(all_tickers)}")

# Save to file
with open('ticker_universe.txt', 'w') as f:
    for ticker in all_tickers:
        f.write(f"{ticker}\n")

print(f"\nSaved {len(all_tickers)} tickers to ticker_universe.txt")
print("\nSample tickers:", ', '.join(all_tickers[:20]))
