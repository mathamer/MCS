from dash import Dash, html, dcc, Input, Output
from urllib.parse import urlparse, parse_qs
import plotly.express as px
import pandas as pd


app = Dash(__name__)
app.layout = html.Div([dcc.Location(id="url"), dcc.Graph(id="graph")])


@app.callback(Output("graph", "figure"), Input("url", "href"))
def callback_func(href):
    parsed_url = urlparse(href)
    captured_value = parse_qs(parsed_url.query)["filename"][0]
    print("captured_value: " + captured_value)
    # Get filename by retrieving parameters from a URL
    df = pd.read_csv("http://localhost:31310/api/files/" + captured_value)

    # Convert timestamp to readable format
    x, y = pd.to_datetime(df["timestamp"], unit="s", utc=True).dt.tz_convert(
        "Europe/Zagreb"
    ), [
        "s1",
        "s2",
        "s3",
        "s4",
        "s5",
        "s6",
    ]
    # Draw graph with plotly.express
    fig = px.line(
        df,
        x=x,
        y=y,
        title="Analysis of " + captured_value,
        labels={"x": "Date", "y": "Value"},
    )

    return fig


app.run_server(debug=False, port=8050, host="0.0.0.0")
