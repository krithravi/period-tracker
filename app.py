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
from dash.dependencies import Input, Output, State
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
lengths = data.Date.diff().dropna().dt.days
# lengths.name = 'Days'

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
pred = last_date + timedelta(days = round(avg_len))

# return later of (today, pred)
if (today > pred):
     pred = today

pred_end = pred + timedelta(days = round(avg_cycle_len))

# return earlier of (early, today)
early = pred - timedelta(days = round(std_len))
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
    name='days',
    marker_color='#299b5b',
    boxpoints='outliers',
    boxmean='sd' # represent mean
))

fig.update_layout(
    xaxis=dict(title='Length in days', zeroline=False),
    title=dict(text='Distribution of cycle lengths')
)

cycle_hist = go.Figure()
cycle_hist.add_trace(go.Histogram(
    x=lengths,
    name='days', # name used in legend and hover labels
    marker_color='#2dc850',
    opacity=0.7,
    yhoverformat = "d days"
))

cycle_hist.update_layout(
    xaxis=dict(title='Length in days'),
    yaxis=dict(title='Count'),
    title=dict(text='Distribution of cycle lengths')
)

# boxplot of period lengths
period_length = go.Figure()
period_length.add_trace(go.Box(
    x=data['Length'],
    name='days',
    marker_color='#289b71',
    boxpoints='outliers',
    boxmean='sd' # represent mean
))

period_length.update_layout(
    xaxis=dict(title='Length in days', zeroline=False),
    title=dict(text='Distribution of period lengths')
)

day_num = (today - last_date).days + 1

# calendars
calendar_one = calendar.month(last_date.year, last_date.month)
calendar_two = calendar.month(last_date.year, last_date.month + 1) if last_date.month <= 11 else calendar.month(last_date.year + 1, 1) 

app.layout = html.Div([
    html.H1("Period Tracker 💚"),
    html.Ul([
        html.Li("Date of last cycle: " + last_date.strftime("%A, %B %d, %Y") + "."),
        html.Ul([
            html.Li("That was " + str((today - last_date).days) + " day(s) ago."),
        ]),

        html.Li("Next predicted cycle: " + pred.strftime("%A, %B %d, %Y") + " to " + pred_end.strftime("%A, %B %d, %Y") + "."),
        html.Ul([
            html.Li("That's in " + str(max(0, (pred - today).days))+ " day(s).")
        ]),

        html.Li("Likely to start as early as " + early.strftime("%A, %B %d, %Y") + "."),
        html.Ul([
            html.Li(" That's in " + str(max(0, (early - today).days)) + " day(s).")
        ]),

        html.Li(["You're on ", html.U("day " + str(day_num)), " of your cycle."]),
        html.Li(fertile_str)
    ]),
    html.Div([
        html.Pre(calendar_one, className="fleft"), 
        html.Pre(calendar_two, className="fright")], className="smush"),
    html.H2("Stats!"),
    html.Ul([
        html.Li("Average cycle length (outliers removed): " + str(avg_len) + " days"),
        html.Li("Cycle length standard deviation (outliers removed): " + str(std_len) + " day(s)"),
        html.Li("Average period length: " + str(round(data.iloc[:, 1].mean(), 2)) + " day(s)")
    ]),
    dcc.Graph(id ="hist-lengths", figure=cycle_hist),
    dcc.Graph(id="box-lengths", figure=fig),
    dcc.Graph(id="period-lengths", figure=period_length),

    html.H2("Submit new entry"),
    html.P("To submit a placeholder entry (if you forgot the date, for example), hit submit without entering a date or length."),
    # dcc.Upload(
    #     id='upload-data',
    #     children=html.Div([
    #         'Drag and Drop or ',
    #         html.A('Select Data File')
    #     ]),
    #     style={
    #         'width': '100%',
    #         'height': '60px',
    #         'lineHeight': '60px',
    #         'borderWidth': '1px',
    #         'borderStyle': 'dashed',
    #         'borderRadius': '5px',
    #         'textAlign': 'center',
    #         'margin': '10px'
    #     },
    #     multiple=False
    # ),

    # dcc.ConfirmDialog(
    #     id='confirm-danger',
    #     message='Do you really want to add this data point? Either the start date is null or the length is 0',
    # ),
    dcc.DatePickerSingle(
        id='date-picker-single',
        max_date_allowed=date.today(),
        initial_visible_month=date.today(),
        clearable=True,
        placeholder="Date"
    ),
    dcc.Input(
        placeholder='Enter the length of the cycle',
        type='number',
        id='input-box',
        min="0"
    ),
    dcc.Textarea(
        id='textarea-example',
        placeholder='Enter a description (optional)',
        style={'width': '100%', 'height': 50}
    ),
    html.Button('Submit', id='button-example-1', style={'cursor': 'pointer'}),
    # html.Div(id='output-danger'),
    html.Div(id='output-container-button',
             children='Enter a value and press submit'),
    html.Footer("Built with lots of love ❤️"),
])

@app.callback(
    Output('output-container-button', 'children'),
    Input('button-example-1', 'n_clicks'),
    State('date-picker-single', 'date'),
    State('input-box', 'value'),
    State('textarea-example', 'value'))
def update_output(n_clicks, date, length, desc):
    # TODO: if both date and length are None, have an alert that says "do you really wanna do this"

    if date is not None and length is not None and length > 0:
        append_string = ""
        if desc:
            append_string = date + ', ' + str(length) + ', ' + desc + '\n'
        else:
            append_string = date + ', ' + str(length) + ', ' + '\n'

        f = open(filename, "a")  # append mode
        f.write(append_string)
        f.close()

        return "Submitted!"
        
    return "Error: either the start date is undefined, or the length is <= 0"
    
    # return 'Start date: {}, Length: {}, Desc: {}'.format(
    #     date,
    #     length,
    #     desc,
    # )

# @app.callback(
#         Output('confirm-danger', 'displayed'),
#         Input('button-example-1', 'n_clicks'),
#         Input('input-box', 'value'),
#         Input('date-picker-single', 'date'))
# def display_confirm(submit, value, date):
#     return submit and (value > 0 or date is None)


# @app.callback(
#         Output('output-danger', 'children'),
#         Input('confirm-danger', 'submit_n_clicks'),
#         State('date-picker-single', 'date'),
#         State('input-box', 'value'),
#         State('textarea-example', 'value'))
# def new_update_output(submit_n_clicks, date, length, desc):
#     if submit_n_clicks:
#         print(filename, date, length, desc)
#         f = open(filename, "a")  # append mode
#         f.write(date + ',' + length + ',' + desc)
#         f.close()

#         return "Submitted!"

if __name__ == "__main__":
    app.run_server(debug=True)
