from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
import plotly.graph_objs as go  # Importing Plotly graph objects

csv_file_path = 'C:\\dash_case\\test_data.csv'

# Read the CSV file into a DataFrame (must be located in the correct folder)
data = pd.read_csv(csv_file_path, delimiter=';')

df = pd.DataFrame(data)


# Convert relevant columns to numeric data types
numeric_columns = ['total calls', 'call answered', 'calls missed']
data[numeric_columns] = data[numeric_columns].apply(pd.to_numeric, errors='coerce')

app = Dash(__name__)

custom_colors = ['#FF5733', '#33FF57']

app.layout = html.Div(children=[
    html.H1(children="Welcome to Callcenter"),
    dcc.Graph(
        figure=px.bar(data, x="Date", y=["call answered", "calls missed"], title='Distribution of Call Center Calls',
                       height=400, color_discrete_sequence=custom_colors,
                       ),
        style={'width': '50%', 'height': '50%'}
    )
])
app.run(debug=True)