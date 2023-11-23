import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import mplfinance as mpf

# Construct the file path
file_path = '/Users/niranjankumar/Desktop/Project/BAJFINANCE.NS.csv'

# Load the CSV file into a DataFrame
df = pd.read_csv(file_path, parse_dates=['Date'])
# Sort the DataFrame by date to ensure the data is in the correct order
df.sort_values('Date', inplace=True)

# Initialize a list to hold the trade details
trades = []

# Loop through the DataFrame starting from the first date we can check for a 3-day inside pattern
for i in range(len(df) - 6):
    # Define the high and low of the first day
    first_day_high = df.loc[i, 'High']
    first_day_low = df.loc[i, 'Low']

    # Check if the second and third days are inside days
    if all(df.loc[i+1:i+2, 'High'] <= first_day_high) and all(df.loc[i+1:i+2, 'Low'] >= first_day_low):
        # Check if the fourth day closes outside the first day's range
        fourth_day_close = df.loc[i+3, 'Close']
        if fourth_day_close > first_day_high or fourth_day_close < first_day_low:
            # A trade has been triggered
            entry_date = df.loc[i+3, 'Date']
            entry = fourth_day_close
            stop_loss = df.loc[i+3,
                               'High'] if fourth_day_close < first_day_low else df.loc[i+3, 'Low']
            target = entry - \
                (2 * (stop_loss - entry)) if fourth_day_close < first_day_low else entry + \
                (2 * (entry - stop_loss))

            # Record the 7th day closing value
            seventh_day_close = df.loc[i+6, 'Close']

            # Determine if the trade is in profit or loss on the 7th day
            trade_result = "Profit" if (fourth_day_close < first_day_low and seventh_day_close < entry) or (
                fourth_day_close > first_day_high and seventh_day_close > entry) else "Loss"
            profit_or_loss_amount = seventh_day_close - entry

            # Add the trade details to the list
            trades.append({
                'Entry_Date': entry_date,
                'Entry': entry,
                'Stop_Loss': stop_loss,
                'Target': target,
                'Seventh_Day_Close': seventh_day_close,
                '1:2': trade_result,
                'Result on 7th Day': profit_or_loss_amount
            })

# Convert the trades list to a DataFrame
trades_df = pd.DataFrame(trades)

# Save the trades DataFrame to a CSV file
output_file = 'trades_output_modified.csv'
trades_df.to_csv(output_file, index=False)

print(f"Trades data saved to {output_file}")
