from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

csv_file_path = 'C:\\dash_case\\test_data.csv'

# Read the CSV file into a DataFrame (must be located in the correct folder)
data = pd.read_csv(csv_file_path, delimiter=';')

df = pd.DataFrame(data)

# X =df['employee active'] 
# X1 =df['emplyee inactive'] 
# Y =df['employee packing'] 

app = Dash(__name__)

custom_colors = ['#FF5733', '#33FF57']

app.layout = html.Div(children=[
    html.H1(children="Welcome to Callcenter"),
    dcc.Graph(
        figure=px.bar(df, x="employee packing", y=["employee active", "emplyee inactive"],
                       barmode='group',
                       height=400, color_discrete_sequence=custom_colors,
                       labels={"employee packing": "Packing", "employee active": "Active", "emplyee inactive": "Inactive"}),
        style={'width': '50%', 'height': '50%'}
    )
])

app.run(debug=True)