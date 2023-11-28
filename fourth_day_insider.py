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

    # Loop through the DataFrame to check for a 4-day inside pattern
    for i in range(len(df) - 7):  # Adjusted range to prevent out-of-range access
        # Define the high and low of the first day
        first_day_high = df.loc[i, 'High']
        first_day_low = df.loc[i, 'Low']

        # Check if the second, third, and fourth days are inside days
        if all(df.loc[i+1:i+3, 'High'] <= first_day_high) and all(df.loc[i+1:i+3, 'Low'] >= first_day_low):
            # Check if the fifth day closes outside the first day's range
            fifth_day_close = df.loc[i+4, 'Close']
            if fifth_day_close > first_day_high or fifth_day_close < first_day_low:
                # A trade has been triggered
                entry_date = df.loc[i+4, 'Date']
                entry = fifth_day_close

                # Using the open value of the breakout day as stop loss
                stop_loss = df.loc[i+4, 'Open']

                # Calculating the target based on the new stop loss
                target = entry - (2 * (stop_loss - entry)) if fifth_day_close < first_day_low else entry + (2 * (entry - stop_loss))

                # Record the 8th day closing value
                eighth_day_close = df.loc[i+7, 'Close']

                # Determine if the trade is in profit or loss on the 8th day
                trade_result = "Profit" if (fifth_day_close < first_day_low and eighth_day_close < entry) or (fifth_day_close > first_day_high and eighth_day_close > entry) else "Loss"
                profit_or_loss_amount = eighth_day_close - entry
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
                    'Eighth_Day_Close': eighth_day_close,
                    'Trade_Result': trade_result,
                    'Profit_or_Loss_Amount': profit_or_loss_amount,
                    'Total Trades': total_trades,
                    'Profitable Trades': profitable_trades,
                    'Loss Trades': loss_trades,
                    'Win Percentage': win_percentage
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
output_folder = '4th_day_insider_results'

# Backtest the stocks
backtest_multiple_stocks(stock_symbols, start_date, end_date, output_folder)