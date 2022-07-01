import dash
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import timedelta, date
from math import ceil
import sys

app = dash.Dash(__name__)

filename = sys.argv[1]
print(filename)

data = pd.read_csv(filename)
data['Date'] = pd.to_datetime(data['Date']).dt.date

# sort by date just in case
data = data.sort_values(by = 'Date')
lengths = data.Date.diff().dropna().astype('timedelta64[D]')

avg_len = round(lengths.mean(), 2)
std_len = round(lengths.std(), 2)
# print("Average cycle length: " + str(avg_len) + " days")
# print("Cycle length std. dev.: " + str(std_len) + " day(s)")
# print("Average period length: " + str(data.iloc[:, 1].mean()))
# print()
today = date.today()
# print("Today's date: ", today)


last_date = data.tail(1)['Date']

pred = last_date + timedelta(days = avg_len)
pred = pred[len(data) - 1]


# return later of (today, pred)
if (today > pred):
     pred = today

# print("Likely to start as early as " + str(pred - timedelta(days = std_len)))
# print("Next predicted start date: " + str(pred))


fig = px.box(x = lengths)

app.layout = html.Div([
    html.H1("App"),
    html.P("Average cycle length: " + str(avg_len) + " days"),
    html.P("Cycle length standard deviation: " + str(std_len) + " day(s)"),
    html.P("Average period length: " + str(data.iloc[:, 1].mean()) + " day(s)"),
    html.P("Distribution of cycle lengths"),
    dcc.Graph(id="life-exp-vs-gdp", figure=fig),
    html.P("Next predicted start date: " + str(pred)),
    html.P("Likely to start as early as " + str(pred - timedelta(days = std_len)))
])


if __name__ == "__main__":
    app.run_server(debug=True)
