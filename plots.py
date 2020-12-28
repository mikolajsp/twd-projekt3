import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px

with open("owner.txt", mode="r", encoding="utf-8") as ownerfile:
    owner = ownerfile.read()

def turn(val, owner):
    if val == owner:
        return "You"
    else:
        return "Someone else"

df = pd.read_csv("messages.csv")
df["who"] = df["author"].apply(turn, args=(owner,))

fig_1 = px.histogram(df, x="date", color="who", title="Your messages over time", labels={"date": "Date", "who": "Who sent the message"})
fig_1.update_yaxes(title_text="Number of messages")


fig_2 = px.histogram(df, x="hour", color="who", range_x=[0, 23], nbins=24,title="Breakdown of messages sent by hour", color_discrete_sequence=["#264653", "#2a9d8f"], labels={"who": "Who sent the message"})
fig_2.update_yaxes(title_text="Number of messages")
fig_2.update_xaxes(title_text="Hour of day", nticks=24)       
fig_2.update_layout(bargap=0.1)


tab1_layout = html.Div([
    html.H2("Overview of your data"),
    dcc.Graph(
        id="default-histogram",
        figure= fig_1),
    dcc.Graph(
        id="hour-histogram",
        figure=fig_2
        )
])

tab2_layout = html.Div([
    dcc.Dropdown(id="person-dropdown"),
    html.Div(
        id="person-histogram-container"
    )
])

app = dash.Dash(__name__)

app.config.suppress_callback_exceptions=True

app.layout = html.Div([
    dcc.Tabs(id="tabs", value="tab1", children=[
    dcc.Tab(label="Your summary", value="tab1"),
    dcc.Tab(label="People", value="tab2"),
    dcc.Tab(label="Groups", value="tab3")
    ]),
    html.Div(id="content")
])

@app.callback(Output("person-dropdown", "options"), [Input("tabs", "value")])
def fill_dropdown(tab):
    if tab == "tab2":
        lis = df.loc[df["thread_type"]=="Regular"].thread_name.unique()
        opts = [ {"label": name, "value" :name} for name in lis]
        return opts

@app.callback(Output("content", "children"), Input("tabs", "value"))
def render_content(tab):
    if tab == "tab1":
        return tab1_layout
    elif tab == "tab2":
        return tab2_layout
    else:
        return html.Div([
            html.H3("Tab 3 content")
        ])

@app.callback(Output("person-histogram-container", "children"), Input("person-dropdown", "value"))
def draw_person_histogram(person):
    if person:
        df_slice = df.loc[df["thread_name"]==person]


        # prepare second histogram
        hour_plot = px.histogram(df_slice, x="hour", color="author", range_x=[0, 23], nbins=24,title="Breakdown of messages sent by hour", color_discrete_sequence=["#264653", "#2a9d8f"], labels={"author": "Author of the message"})
        hour_plot.update_yaxes(title_text="Number of messages")
        hour_plot.update_xaxes(title_text="Hour of day", nticks=24)       
        hour_plot.update_layout(bargap=0.1)


        return [dcc.Graph(id="person-histogram",
            figure=px.histogram(df_slice, x="date", color="author")
            ),
            dcc.Graph(id="person-hour-histogram",
            figure=hour_plot)
        ]

if __name__ == "__main__":
    app.run_server(debug=True)
