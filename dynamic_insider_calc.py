import yfinance as yf
import pandas as pd
import os

def backtest_stock(stock_symbol, start_date, end_date, output_folder):
    # Fetch the stock data
    df = yf.download(stock_symbol, start=start_date, end=end_date)
    df.reset_index(inplace=True)

    # Initialize a list to hold the trade details
    trades = []
    total_trades = 0
    profitable_trades = 0
    loss_trades = 0

    # Loop through the DataFrame to check for a 3-day inside pattern
    for i in range(len(df) - 8):  # Adjusted range to avoid out-of-range access
        # Define the high and low of the first day
        first_day_high = df.loc[i, 'High']
        first_day_low = df.loc[i, 'Low']

        # Check if the second, third, and fourth days are inside days
        if all(df.loc[i+1:i+3, 'High'] <= first_day_high) and all(df.loc[i+1:i+3, 'Low'] >= first_day_low):
            insider_days = 3  # Initialize insider days count

            # Check for breakout/breakdown from the fifth day onwards
            breakout_day = None
            for j in range(4, 7):  # Check for breakout/breakdown on 5th, 6th, and 7th day
                day_close = df.loc[i+j, 'Close']
                if day_close > first_day_high or day_close < first_day_low:
                    breakout_day = j
                    break
                else:
                    insider_days += 1

            if breakout_day is not None and i + breakout_day + 2 < len(df):
                # A trade has been triggered
                entry_date = df.loc[i+breakout_day, 'Date']
                entry = df.loc[i+breakout_day, 'Close']

                # Using the open value of the breakout day as stop loss
                stop_loss = df.loc[i+breakout_day, 'Open']
                # Calculating the target based on the new stop loss
                target = entry - (2 * (stop_loss - entry)) if entry < first_day_low else entry + (2 * (entry - stop_loss))

                # Record the closing value two days after the breakout
                closing_day_close = df.loc[i+breakout_day+2, 'Close']

                # Determine if the trade is in profit or loss
                trade_result = "Profit" if (entry < first_day_low and closing_day_close < entry) or (entry > first_day_high and closing_day_close > entry) else "Loss"
                profit_or_loss_amount = closing_day_close - entry
                total_trades += 1

                # Increment profitable or loss trades
                if trade_result == "Profit":
                    profitable_trades += 1
                else:
                    loss_trades += 1

                # Calculate win percentage
                win_percentage = (profitable_trades / total_trades * 100)

                # Add the trade details to the list
                trades.append({
                    'Entry_Date': entry_date,
                    'Entry': entry,
                    'Stop_Loss': stop_loss,
                    'Target': target,
                    'Closing_Day_Close': closing_day_close,
                    'Trade_Result': trade_result,
                    'Profit_or_Loss_Amount': profit_or_loss_amount,
                    'Total Trades': total_trades,
                    'Profitable Trades': profitable_trades,
                    'Loss Trades': loss_trades,
                    'Win Percentage': win_percentage,
                    'Insider Days': insider_days  # Added field for insider days count
                })

    # Convert the trades list to a DataFrame
    trades_df = pd.DataFrame(trades)

    # Save the trades DataFrame to a CSV file
    output_file = os.path.join(output_folder, f'{stock_symbol}_trades.csv')
    trades_df.to_csv(output_file, index=False)

    print(f"Trades data saved to {output_file}")

def backtest_multiple_stocks(stock_symbols, start_date, end_date, output_folder):
    for stock_symbol in stock_symbols:
        backtest_stock(stock_symbol, start_date, end_date, output_folder)

# List of stock symbols
stock_symbols = ['ICICIBANK.NS', 'RELIANCE.NS', 'BAJAJ-AUTO.NS', 'MARUTI.NS', 'LTIM.NS',
                 'TITAN.NS', 'ULTRACEMCO.NS', 'NTPC.NS', 'TATACONSUM.NS', 'KOTAKBANK.NS', 'HDFCLIFE.NS',
                 'COALINDIA.NS', 'TATASTEEL.NS', 'BAJFINANCE.NS', 'BAJAJFINSV.NS', 'ITC.NS',
                    'HEROMOTOCO.NS', 'INDUSINDBK.NS', 'NESTLEIND.NS',
                 'TECHM.NS', 'ONGC.NS', 'BRITANNIA.NS', 'HINDALCO.NS', 'TCS.NS', 'APOLLOHOSP.NS',
                 'WIPRO.NS', 'CIPLA.NS', 'ADANIENT.NS']

# Specify the start and end dates
start_date = '2018-01-01'
end_date = '2023-11-20'

# Specify the output folder
output_folder = 'Backtest_Results'

# Backtest the stocks
backtest_multiple_stocks(stock_symbols, start_date, end_date, output_folder)