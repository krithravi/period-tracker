######################### START IMPORTS           #########################
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
######################### END IMPORTS             #########################

######################### START USER MODIFICATION ######################### 
show_fertile  = True
calendar.setfirstweekday(calendar.SUNDAY)
fertile_window_length = 5
fertile_window_num_days_prior  = 14
######################### END   USER MODIFICATION ######################### 


app = dash.Dash(__name__)
app.title = 'Period Tracker'

filename = sys.argv[1]
print("Reading from: " + filename)

data = pd.read_csv(filename)
data['Date'] = pd.to_datetime(data['Date']).dt.date

# sort by date just in case
data = data.sort_values(by = 'Date')
lengths = data.Date.diff().dropna().astype('timedelta64[D]')
lengths.name = 'Days'

# filtering outliers by 1.5 IQR rule
def filter_outliers(data):
    Q1, Q3 = data.quantile([.25, .75])
    IQR = Q3 - Q1

    filtered = data.loc[lambda x: (x <= Q3 + 1.5 * IQR) & (x >= Q1 - 1.5 * IQR)]
    print(len(data) - len(filtered), "outlier(s) detected")
    return filtered

no_outlier_lengths = filter_outliers(lengths)

avg_len = round(no_outlier_lengths.mean(), 2)
std_len = round(no_outlier_lengths.std(), 2)
avg_cycle_len = round(filter_outliers(data['Length']).mean(), 2)

today = date.today()
last_date = data.tail(1)['Date'][len(data) - 1]
pred = last_date + timedelta(days = avg_len)

# return later of (today, pred)
if (today > pred):
     pred = today

pred_end = pred + timedelta(days = avg_cycle_len)

# return earlier of (early, today)
early = pred - timedelta(days = std_len)
if (early < today):
    early = today

# computes a fertile window
if show_fertile:
    fertile_start = pred - timedelta(days = fertile_window_num_days_prior)
    fertile_end   = fertile_start + timedelta(days = fertile_window_length)
    fertile_str   = "Fertile window: " + fertile_start.strftime("%A, %B %d, %Y") + " to " + fertile_end.strftime("%A, %B %d, %Y") 
else:
    fertile_str = "Woooo"

# boxplot of cycle lengths
fig = go.Figure()
fig.add_trace(go.Box(
    x=lengths,
    name='Days',
    marker_color='#299b5b',
    boxpoints='outliers',
    boxmean='sd' # represent mean
))

fig.update_layout(
    xaxis=dict(title='Length in days', zeroline=False),
    title=dict(text='Distribution of cycle lengths')
)

# boxplot of period lengths
period_length = go.Figure()
period_length.add_trace(go.Box(
    x=data['Length'],
    name='Days',
    marker_color='#289b71',
    boxpoints='outliers',
    boxmean='sd' # represent mean
))

period_length.update_layout(
    xaxis=dict(title='Length in days', zeroline=False),
    title=dict(text='Distribution of period lengths')
)


day_num = (today - last_date).days + 1

app.layout = html.Div([
    html.H1("Period Tracker 💚"),
    html.Ul([
        html.Li("Date of last cycle: " + last_date.strftime("%A, %B %d, %Y") + "."),
        html.Ul([
            html.Li("That was " + str((today - last_date).days) + " day(s) ago."),
        ]),

        html.Li("Next predicted cycle: " + pred.strftime("%A, %B %d, %Y") + " to " + pred_end.strftime("%A, %B %d, %Y") + "."),
        html.Ul([
            html.Li("That's in " + str((pred - today).days)+ " day(s).")
        ]),

        html.Li("Likely to start as early as " + early.strftime("%A, %B %d, %Y") + "."),
        html.Ul([
            html.Li(" That's in " + str((early - today).days) + " day(s).")
        ]),

        html.Li(["You're on ", html.U("day " + str(day_num)), " of your cycle."]),
        html.Li(fertile_str)
    ]),
    html.Div([
        html.Pre(calendar.month(last_date.year, last_date.month), className="fleft"), 
        html.Pre(calendar.month(pred.year, pred.month), className="fright")], className="smush"),
    html.H2("Stats!"),
    html.Ul([
        html.Li("Average cycle length (outliers removed): " + str(avg_len) + " days"),
        html.Li("Cycle length standard deviation (outliers removed): " + str(std_len) + " day(s)"),
        html.Li("Average period length: " + str(round(data.iloc[:, 1].mean(), 2)) + " day(s)")
    ]),
    dcc.Graph(id="box-lengths", figure=fig),
    dcc.Graph(id="period-lengths", figure=period_length),
    html.Footer("Built with lots of love ❤️")

])

if __name__ == "__main__":
    app.run_server(debug=True)
