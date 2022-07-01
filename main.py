import pandas as pd
import numpy as np
from datetime import timedelta
from datetime import date
import sys

filename = sys.argv[1]
print("Reading from: " + filename)
print()

data = pd.read_csv(filename)
data['Date'] = pd.to_datetime(data['Date']).dt.date

# sort by date just in case
data = data.sort_values(by = 'Date')

lengths = data.Date.diff().dropna()

avg_len = lengths.mean().days
std_len = lengths.std().days
print("Average cycle length: " + str(avg_len) + " days")
print("Cycle length std. dev.: " + str(std_len) + " day(s)")
print("Average period length: " + str(data.iloc[:, 1].mean()))
print()
today = date.today()
print("Today's date: ", today)


last_date = data.tail(1)['Date']

pred = last_date + timedelta(days = avg_len)
pred = pred[len(data) - 1]


# return later of (today, pred)
if (today > pred):
     pred = today

print("Next predicted start date: " + str(pred))

tmp = pred - timedelta(days = std_len)
print(tmp)
