from dash import Dash, html, dcc
import dash
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# Read the CSV file into a pandas DataFrame
df = pd.read_csv('test_data.csv', delimiter=';')

app = Dash(__name__)

app.layout = html.Div(children=[
    html.H1(children="Customers in Queue"),#TA BORT?!
    dcc.Graph(id='queue-graph', config={'displayModeBar': False}),
])

@app.callback(
    Output('queue-graph', 'figure'),
    Input('queue-graph', 'relayoutData')
)
def update_graph(relayoutData):
    column_name = 'Que amount'
    value = df.at[0, column_name]
    data = [
        go.Bar(
            x=[column_name],
            y=[value],
            text=str(value),
            textposition='inside',  # Display the number above the bar
            marker=dict(color='royalblue'),
            textfont={'size': 80}  # Adjust the font size here
        
        )
    ]
    layout = go.Layout(
        title=f'Customers in que',

        bargap=0.1
    )
    return {'data': data, 'layout': layout}

if __name__ == '__main__':
    app.run_server(debug=True)
