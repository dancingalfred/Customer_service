import os
import pandas as pd
from dash import Dash, html, Input, Output, dcc

CURR_DIR_PATH = os.path.dirname(os.path.realpath(__file__))

dummy_calls = pd.read_csv(CURR_DIR_PATH+'\\'+'test_data.csv', delimiter=';')

df = pd.DataFrame(dummy_calls)
app = Dash(__name__)

app.layout = html.Div([
    html.H2("Samtal"),
    html.Div(id='besvarade'),
    dcc.Interval(
        id='interval-component',
        interval=1 * 10000,  # Interval in milliseconds (e.g., every 1 second)
        n_intervals=0  # Initial number of intervals
    )
])

@app.callback(
    Output('besvarade', 'children'),
    Input('interval-component', 'n_intervals')
)
def update_live_number(n_intervals):
    besvarade = df['call answered'].iloc[1]
    missade = df['calls missed'].iloc[1]
    return f"Besvarade: {besvarade}\nMissade: {missade}"

if __name__ == '__main__':
    app.run_server(debug=True)