import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px


def turn(val):
    if val == "Mikołaj Spytek":
        return "you"
    else:
        return "someone else"


df = pd.read_csv("messages.csv")

df["who"] = df["author"].apply(turn)




fig = px.histogram(df, x="date", color="who")
fig.show()



app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Tabs(id="tabs", value="tab1", children=[
    dcc.Tab(label="Your summary", value="tab1"),
    dcc.Tab(label="People", value="tab2"),
    dcc.Tab(label="Groups", value="tab3")
    ]),
    html.Div(id="content")
])

@app.callback(Output("content", "children"), Input("tabs", "value"))
def render_content(tab):
    if tab == "tab1":
        return html.Div([
            html.H3("Tab 1 content")
        ])
    elif tab == "tab2":
        return html.Div([
            html.H3("Tab 2 content")
        ])
    else:
        return html.Div([
            html.H3("Tab 3 content")
        ])

if __name__ == "__main__":
    app.run_server(debug=True)
    
