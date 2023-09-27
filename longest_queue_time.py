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
    html.H1(children="Dashboard"),  # Update the title as needed
    dcc.Graph(id='queue-graph', config={'displayModeBar': False}),
    dcc.Graph(id='speed-indicator', config={'displayModeBar': False})
])

@app.callback(
    [Output('queue-graph', 'figure'),
     Output('speed-indicator', 'figure')],
    [Input('queue-graph', 'relayoutData')]
)
def update_graph(relayoutData):
    # Update the queue graph
    column_name = 'Que amount'
    value = df.at[0, column_name]
    queue_data = [
        go.Bar(
            x=[column_name],
            y=[value],
            text=str(value),
            textposition='inside',  # Display the number above the bar
            marker=dict(color='royalblue'),
            textfont={'size': 80}  # Adjust the font size here
        )
    ]
    queue_layout = go.Layout(
        title=f'Longest Queue time',
        bargap=0.1
    )

    # Update the speed indicator graph
    value_longest_wait = df.at[0, 'longest wait']
    speed_data = [
        go.Indicator(
            mode="gauge+number+delta",
            value=float(value_longest_wait),
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Minutes", 'font': {'size': 24}},
            # delta={'reference': int(value_longest_wait), 'increasing': {'color': "RebeccaPurple"}},
            gauge={
                'axis': {'range': [None, 60], 'tickwidth': 1, 'tickcolor': "darkblue"},
                'bar': {'color': "darkblue"},
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "gray",
                'steps': [
                    {'range': [0, 5], 'color': 'green'},
                    {'range': [5, 15], 'color': 'orange'},
                    {'range': [15, 60], 'color': 'red'}],
                'threshold': {
                    'line': {'color': "gold", 'width': 4},
                    'thickness': 0.75,
                    'value': int(value_longest_wait)
                }
            }
        )
    ]
    speed_layout = go.Layout(
        title="Longest Queue Time",
        paper_bgcolor="lavender",
        font={'color': "darkblue", 'family': "Arial"}
    )

    return {'data': queue_data, 'layout': queue_layout}, {'data': speed_data, 'layout': speed_layout}

if __name__ == '__main__':    app.run_server(debug=True)
