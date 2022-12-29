import dash
from dash import dcc, html, dash_table
from collections import Counter
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from dash.dependencies import Output, Input
import time
# Example on how you might use the API to visualise data from a cisco device. 
# Create a function to retrieve the data

# you should add a function to cache the data. It should only reload sometimes.
def get_data():
    import requests

    url = "http://localhost:8000/do_device_command"
    form_data = {
        "devices": "example1",
        "commands": "show interfaces",
        "enable_mode": False,
        "parse": True,
        "conft": False
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    response = requests.post(url, data=form_data, headers=headers)
    return response.json()

# Create a function to generate the charts
def generate_charts(data):
    # Flatten the data list to a single list of dictionaries
    interfaces = [d for sublist in data for sublist in sublist for d in sublist]

    # Create a pie chart showing the distribution of hardware types
    hardware_types = [d['hardware_type'] for d in interfaces]
    hardware_counts = Counter(hardware_types)
    hardware_df = pd.DataFrame.from_dict(hardware_counts, orient='index').reset_index()
    hardware_df.columns = ['Hardware Type', 'Count']
    hardware_pie = px.pie(hardware_df, values='Count', names='Hardware Type')

    # Create a donut chart showing the distribution of link statuses
    link_statuses = [d['link_status'] for d in interfaces]
    link_counts = Counter(link_statuses)
    link_df = pd.DataFrame.from_dict(link_counts, orient='index').reset_index()
    link_df.columns = ['Link Status', 'Count']
    link_donut = px.pie(link_df, values='Count', names='Link Status', hole=.4)

    # Create a subplot to combine the two charts
    fig = make_subplots(rows=1, cols=2, specs=[[{'type': 'pie'}, {'type': 'pie'}]])
    fig.add_trace(go.Pie(values=hardware_pie['data'][0]['values'], labels=hardware_pie['data'][0]['labels'], name='Hardware Types'), row=1, col=1)
    fig.add_trace(go.Pie(values=link_donut['data'][0]['values'], labels=link_donut['data'][0]['labels'], name='Link Statuses'), row=1, col=2)
    fig.update_layout(title_text='Network Interface Summary')
    return fig

def generate_table(data):
    # Flatten the data list to a single list of dictionaries
    interfaces = [d for sublist in data for sublist in sublist for d in sublist]

    # Create a dataframe from the interface data
    df = pd.DataFrame(interfaces)

    # Select the columns to include in the table
    columns = ['interface', 'link_status', 'protocol_status', 'hardware_type', 'address', 'description', 'mtu', 'ip_address', 'crc']

    # Create the Dash table
    table = dash_table.DataTable(
        id='table',
        columns=[{'name': c, 'id': c} for c in columns],
        data=df[columns].to_dict('records'),
        style_cell={'textAlign': 'left'},
        style_data_conditional=[
            {
                'if': {'column_id': 'protocol_status', 'filter_query': '{protocol_status} eq "up"'},
                'color': 'green'
            },
            {
                'if': {'column_id': 'protocol_status', 'filter_query': '{protocol_status} eq "down"'},
                'color': 'red'
            },
            {
                'if': {'column_id': 'link_status', 'filter_query': '{link_status} eq "up"'},
                'color': 'green'
            },
            {
                'if': {'column_id': 'link_status', 'filter_query': '{link_status} eq "down"'},
                'color': 'red'
            },
             {        
                'if': {'column_id': 'link_status', 'filter_query': '{link_status} eq "administratively down"'},
                'display': 'none'
            }
        ]
    )
    return table




# Initialize the Dash app
app = dash.Dash()

# Loads data
data = get_data()

# Create the Dash layout
app.layout = html.Div(
    children=[
        html.H1(children='Cisco Device Interface status'),
        html.Button('Refresh data', id='refresh-button'),
        dcc.Graph(id='charts', figure=generate_charts(data)),
        html.H2(children='Interface Details'),
        generate_table(data)
    ]
)

@app.callback(
    [Output('table', 'data')],
    [Input('refresh-button', 'n_clicks_timestamp')]
)

def refresh_data(n_clicks_timestamp):
    if not n_clicks_timestamp or time.time() - n_clicks_timestamp > 300:
        data = get_data()
    # If 5 minutes have not elapsed, do not update the table data
    return [generate_table(data).data]

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
    
    
