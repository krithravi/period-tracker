import dash
from dash import dcc, html
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import timedelta, date
from math import ceil
import calendar
import sys

app = dash.Dash(__name__)
app.title = 'Period Tracker'

calendar.setfirstweekday(calendar.SUNDAY)

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
today = date.today()
# print("Today's date: ", today)


last_date = data.tail(1)['Date'][len(data) - 1]

pred = last_date + timedelta(days = avg_len)


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
    marker_color='#299b5b',
    boxmean='sd' # represent mean
))

fig.update_layout(
    xaxis=dict(title='Length in days', zeroline=False),
    title=dict(text='Distribution of cycle lengths')
)

day_num = (today - last_date).days + 1

app.layout = html.Div([
    html.H1("Period Tracker 💚"),
    html.Ul([
        html.Li("Date of last cycle: " + last_date.strftime("%A, %B %d, %Y") + ". That was " + str((last_date - today).days * -1) + " day(s) ago."),
        html.Li("Next predicted start date: " + pred.strftime("%A, %B %d, %Y") + ". That's in " + str((pred - today).days)+ " day(s)."),
        html.Li("Likely to start as early as " + early.strftime("%A, %B %d, %Y") + ". That's in " + str((early - today).days) + " day(s)."),
        html.Li(["You're on ", html.U("day " + str(day_num)), " of your cycle."])
    ]),
    html.Div([html.Pre(calendar.month(today.year, today.month), className="fleft"), html.Pre(calendar.month(pred.year, pred.month), className="fright")], className="smush"),
    html.H2("Stats!"),
    html.Ul([
        html.Li("Average cycle length: " + str(avg_len) + " days"),
        html.Li("Cycle length standard deviation: " + str(std_len) + " day(s)"),
        html.Li("Average period length: " + str(round(data.iloc[:, 1].mean(), 2)) + " day(s)")
    ]),
    dcc.Graph(id="box-lengths", figure=fig)

])

if __name__ == "__main__":
    app.run_server(debug=True)
