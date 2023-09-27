import os
import pandas as pd
from dash import Dash, html, Input, Output, dcc
import dash.dependencies as dd

CURR_DIR_PATH = os.path.dirname(os.path.realpath(__file__))

dummy_calls = pd.read_csv(CURR_DIR_PATH+'\\'+'test_data.csv')

df = pd.DataFrame(dummy_calls)
app = Dash(__name__)

app.layout = html.Div([
    html.H1("Besvarade samtal"),
    html.Div(id='live-update-text'),
    dcc.Interval(
        id='interval-component',
        interval=1 * 10000,  # Interval in milliseconds (e.g., every 1 second)
        n_intervals=0  # Initial number of intervals
    )
])

@app.callback(
    Output('live-update-text', 'children'),
    Input('interval-component', 'n_intervals')
)
def update_live_number(n_intervals):

    latest_number = df['time'].iloc[1]

    return f"Number: {latest_number}"

if __name__ == '__main__':
    app.run_server(debug=True)