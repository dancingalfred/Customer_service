import os
import pandas as pd
from dash import Dash, html, Input, Output, dcc
import plotly.express as px

CURR_DIR_PATH = os.path.dirname(os.path.realpath(__file__))

dummy_calls = pd.read_csv(CURR_DIR_PATH+'\\'+'test_data.csv', delimiter=';')

df = pd.DataFrame(dummy_calls)

fig=px.bar(df, x='Date', y=['call answered', 'calls missed', 'longest wait'])
fig.update_layout(legend_title_text='Monthly calls')
fig.update_yaxes(title_text='Calls')
app = Dash(__name__)

app.layout = html.Div([
    html.H2("Last month"),
    dcc.Graph(
        id='line_plot',
        figure=fig),
])

if __name__ == '__main__':
    app.run_server(debug=True)