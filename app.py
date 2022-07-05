import dash
from dash import dcc
from dash import html
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import timedelta, date
from math import ceil
import sys

app = dash.Dash(__name__)

filename = sys.argv[1]
print("Reading from: " + filename)

data = pd.read_csv(filename)
data['Date'] = pd.to_datetime(data['Date']).dt.date

# sort by date just in case
data = data.sort_values(by = 'Date')
lengths = data.Date.diff().dropna().astype('timedelta64[D]')
lengths.name = 'Days'

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


early = pred - timedelta(days = std_len)
if (today > early):
    early = today
# print("Likely to start as early as " + str(early))
# print("Next predicted start date: " + str(pred))


fig = go.Figure()
fig.add_trace(go.Box(
    x=lengths,
    name='Days',
    marker_color='lightseagreen',
    boxmean='sd' # represent mean
))

fig.update_layout(
    xaxis=dict(title='Length in days', zeroline=False),
    title=dict(text='Distribution of cycle lengths')
)

app.layout = html.Div([
    html.H1("Period Tracker App"),
    html.P("Average cycle length: " + str(avg_len) + " days"),
    html.P("Cycle length standard deviation: " + str(std_len) + " day(s)"),
    html.P("Average period length: " + str(round(data.iloc[:, 1].mean(), 2)) + " day(s)"),
    # html.P("Distribution of cycle lengths"),
    dcc.Graph(id="box-lengths", figure=fig),
    html.P("Next predicted start date: " + pred.strftime("%A, %B %d, %Y")),
    html.P("That's in " + str((pred - today))[:-9] + "!"),
    html.P("Likely to start as early as " + early.strftime("%A, %B %d, %Y"))
    # html.H2("Enter a new record!")

])


if __name__ == "__main__":
    app.run_server(debug=True)
