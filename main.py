import os
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from dash import Dash, html, Input, Output, dcc

CURR_DIR_PATH = os.path.dirname(os.path.realpath(__file__))

dummy_calls = pd.read_csv(CURR_DIR_PATH+'\\'+'test_data.csv', delimiter=';')

df = pd.DataFrame(dummy_calls)
month_fig=px.bar(df, x='Date', y=['call answered', 'calls missed', 'longest wait']) # monthly data
month_fig.update_layout(legend_title_text='Monthly calls')
month_fig.update_yaxes(title_text='Calls')

numeric_columns = ['total calls', 'call answered', 'calls missed'] #daily data
df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric, errors='coerce')

app = Dash(__name__)

custom_colors = ['#FF5733', '#33FF57']

app.layout = html.Div([
    html.H3("Giggle Gear"),
    html.Div([
    dcc.Graph( #Shows who in an call, whos waiting and whos available
        figure=px.bar(df, x="employee packing", y=["employee active", "emplyee inactive"],
                       barmode='group',
                       height=400, color_discrete_sequence=custom_colors,
                       labels={"employee packing": "Packing", "employee active": "Active", "emplyee inactive": "Inactive"}),
        style={'width': '50%', 'height': '50%'}
    ),
    html.Div(id='besvarade'), # shows answered and missed calls
    dcc.Interval(
        id='interval-component',
        interval=1 * 10000,  
        n_intervals=0  
    ),
    dcc.Graph(id='queue-graph', config={'displayModeBar': False}), # Display maximum waiting
], style={'display':'flex'}),
html.Div([
    dcc.Graph( # monthly data
        id='line_plot',
        figure=month_fig),
    dcc.Graph( # Daily data
        figure=px.bar(df, x="Date", y=["call answered", "calls missed"], title='Distribution of Call Center Calls',
                       height=400, color_discrete_sequence=custom_colors,
                       ),
        style={'width': '50%', 'height': '50%'}
    ),
    dcc.Graph(id='speed-indicator', config={'displayModeBar': False}, style={'width': '50%', 'height': '50%'}), #Display warning
    
], style={'display':'flex'})
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


@app.callback(
    Output('besvarade', 'children'),
    Input('interval-component', 'n_intervals')
)
def update_live_number(n_intervals): # pick answerd and missed calls from a certain moment in time.
    besvarade = df['call answered'].iloc[1] 
    missade = df['calls missed'].iloc[1]
    return f"Besvarade: {besvarade}\nMissade: {missade}"


if __name__ == '__main__':
    app.run_server(debug=True)