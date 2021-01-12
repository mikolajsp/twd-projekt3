import dash
import os
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud
from datetime import datetime

# HELPER FUNCTIONS


def generateMessageOwner(val, owner):
    if val == owner:
        return "Sent"
    else:
        return "Received"


def generalTimeHistogram():
    timeHistogram = px.histogram(df, x="date", color="who", title="Your messages over time", labels={
        "date": "Date", "who": "Number of messages:"})
    timeHistogram.update_yaxes(title_text="Number of messages")
    timeHistogram.update_layout(hovermode="x")
    timeHistogram.update_traces(hovertemplate='Number of messages: %{y}')
    return timeHistogram


def generalHourHistogram():
    hourHistogram = px.histogram(df, x="hour", color="who", range_x=[-0.5, 23.5], nbins=24,
                                 title="Breakdown of messages sent by hour",
                                 color_discrete_sequence=[
                                     "#264653", "#2a9d8f"],
                                 labels={"who": "Number of messages:"})
    hourHistogram.update_yaxes(title_text="Number of messages")
    hourHistogram.update_xaxes(
        title_text="Hour of day", nticks=24, tickmode='linear', tick0=0.0, dtick=1.0)
    hourHistogram.update_layout(hovermode="x", bargap=0.1)
    hourHistogram.update_traces(hovertemplate='Number of messages: %{y}')

    return hourHistogram


def generateWordCloudImage(thread, isowner):
    wcimg = None
    df_slice = df.loc[df["thread_name"] == thread]
    if isowner:
        text = df_slice.loc[df_slice["author"]
                            == owner].content.str.cat(sep=" ")
    else:
        text = df_slice.loc[df_slice["author"]
                            != owner].content.str.cat(sep=" ")
    if len(text) > 0:
        wordcloud = WordCloud(
            width=1200,
            height=600,
            background_color="rgba(255, 255, 255, 0)",
            mode="RGBA",
            stopwords=stop_words,
            collocations=False).generate(text)
        wcimg = wordcloud.to_image()
    return wcimg


def generateStatistics():
    endDateString = df["date"].max()
    startDateString = df["date"].min()
    startDate = datetime.fromisoformat(startDateString)
    endDate = datetime.fromisoformat(endDateString)
    startDateFormated = startDate.strftime("%A, the %d. %B %Y")
    endDateFormated = endDate.strftime("%A, the %d. %B %Y")
    numYourMsg = len(df.loc[df["author"] == owner])
    numTheirMsg = len(df.loc[df["author"] != owner])
    daysNum = abs(endDate - startDate).days
    avgYourMsgPerDay = numYourMsg/daysNum
    avgYourWordCount = df.loc[df["author"] == owner, "words"].mean()
    avgYourCharCount = df.loc[df["author"] == owner, "chars"].mean()
    avgTheirMsgPerDay = numTheirMsg/daysNum
    avgTheirWordCount = df.loc[df["author"] != owner, "words"].mean()
    avgTheirCharCount = df.loc[df["author"] != owner, "chars"].mean()

    return """
    # Statistics
    We're analyzing your data from **{}**, to  **{}**, that is **{} days**.

    In that time period **you sent {} messages** and **received {} messages**. That makes a total of {} messeges.

    On average, **you've written {:.2f} messages per day**, and each of those consisted on average of {:.2f} words, or {:.2f} characters.

    On the other hand, **you've received {:.2f} messages per day**, and each of those consisted on average of {:.2f} words, or {:.2f} characters.
    

    """.format(startDateFormated,
               endDateFormated,
               daysNum,
               numYourMsg,
               numTheirMsg,
               numTheirMsg+numYourMsg,
               avgYourMsgPerDay,
               avgYourWordCount,
               avgYourCharCount,
               avgTheirMsgPerDay,
               avgTheirWordCount,
               avgTheirCharCount)

# PREPARING GLOBAL VARIABLES


# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
external_stylesheets = [dbc.themes.BOOTSTRAP]

# words not to include in the wordclouds sourced from
# https://github.com/fergiemcdowall/stopword
stop_words = [
    'a', 'aby', 'ach', 'acz', 'aczkolwiek', 'aj', 'albo', 'ale', 'ależ', 'ani', 'sie',
    'aż', 'bardziej', 'bardzo', 'bo', 'bowiem', 'by', 'byli', 'bynajmniej',
    'być', 'był', 'była', 'było', 'były', 'będzie', 'będą', 'cali', 'cała',
    'cały', 'ci', 'cię', 'ciebie', 'co', 'cokolwiek', 'coś', 'czasami',
    'czasem', 'czemu', 'czy', 'czyli', 'daleko', 'dla', 'dlaczego', 'dlatego',
    'do', 'dobrze', 'dokąd', 'dość', 'dużo', 'dwa', 'dwaj', 'dwie', 'dwoje',
    'dziś', 'dzisiaj', 'gdy', 'gdyby', 'gdyż', 'gdzie', 'gdziekolwiek',
    'gdzieś', 'i', 'ich', 'ile', 'im', 'inna', 'inne', 'inny', 'innych', 'iż',
    'ja', 'ją', 'jak', 'jakaś', 'jakby', 'jaki', 'jakichś', 'jakie', 'jakiś',
    'jakiż', 'jakkolwiek', 'jako', 'jakoś', 'je', 'jeden', 'jedna', 'jedno',
    'jednak', 'jednakże', 'jego', 'jej', 'jemu', 'jest', 'jestem', 'jeszcze',
    'jeśli', 'jeżeli', 'już', 'ją', 'każdy', 'kiedy', 'kilka', 'kimś', 'kto',
    'ktokolwiek', 'ktoś', 'która', 'które', 'którego', 'której', 'który',
    'których', 'którym', 'którzy', 'ku', 'lat', 'lecz', 'lub', 'ma', 'mają',
    'mało', 'mam', 'mi', 'mimo', 'między', 'mną', 'mnie', 'mogą', 'moi', 'moim',
    'moja', 'moje', 'może', 'możliwe', 'można', 'mój', 'mu', 'musi', 'my', 'na',
    'nad', 'nam', 'nami', 'nas', 'nasi', 'nasz', 'nasza', 'nasze', 'naszego',
    'naszych', 'natomiast', 'natychmiast', 'nawet', 'nią', 'nic', 'nich', 'nie',
    'niech', 'niego', 'niej', 'niemu', 'nigdy', 'nim', 'nimi', 'niż', 'no', 'o',
    'obok', 'od', 'około', 'on', 'ona', 'one', 'oni', 'ono', 'oraz', 'oto',
    'owszem', 'pan', 'pana', 'pani', 'po', 'pod', 'podczas', 'pomimo', 'ponad',
    'ponieważ', 'powinien', 'powinna', 'powinni', 'powinno', 'poza', 'prawie',
    'przecież', 'przed', 'przede', 'przedtem', 'przez', 'przy', 'roku',
    'również', 'sam', 'sama', 'są', 'się', 'skąd', 'sobie', 'sobą', 'sposób',
    'swoje', 'ta', 'tak', 'taka', 'taki', 'takie', 'także', 'tam', 'te', 'tego',
    'tej', 'temu', 'ten', 'teraz', 'też', 'to', 'tobą', 'tobie', 'toteż',
    'trzeba', 'tu', 'tutaj', 'twoi', 'twoim', 'twoja', 'twoje', 'twym', 'twój',
    'ty', 'tych', 'tylko', 'tym', 'u', 'w', 'wam', 'wami', 'was', 'wasz', 'zaś',
    'wasza', 'wasze', 'we', 'według', 'wiele', 'wielu', 'więc', 'więcej', 'tę',
    'wszyscy', 'wszystkich', 'wszystkie', 'wszystkim', 'wszystko', 'wtedy',
    'wy', 'właśnie', 'z', 'za', 'zapewne', 'zawsze', 'ze', 'zł', 'znowu',
    'znów', 'został', 'żaden', 'żadna', 'żadne', 'żadnych', 'że', 'żeby',
    '$', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '_']

basedirectory = os.path.dirname(os.path.abspath(__file__))

# getting the messages 'owners' name
ownernamepath = os.path.join(basedirectory, "owner.txt")
with open(ownernamepath, mode="r", encoding="utf-8") as ownerfile:
    owner = ownerfile.read()

# preparing reactions dataframe
reactionfile = os.path.join(basedirectory, "reactions.csv")
df_reactions = pd.read_csv(reactionfile)
df_reactions["who"] = df_reactions["reacting_person"].apply(
    generateMessageOwner, args=(owner,))

# preparing main messages dataframe
messagefile = os.path.join(basedirectory, "messages.csv")
df = pd.read_csv(messagefile)
df["who"] = df["author"].apply(generateMessageOwner, args=(owner,))

# LAYOUT TEMPLATES FOR EACH TAB

tab1_layout = html.Div([
    html.H2("Overview of your data"),
    dcc.Graph(
        id="default-histogram",
        figure=generalTimeHistogram()
    ),
    dcc.Graph(
        id="hour-histogram",
        figure=generalHourHistogram()
    ),
    dcc.Markdown(
        generateStatistics()
    )
])

tab2_layout = html.Div([
    html.H2("Data of a private conversation thread"),


    html.Div(
        id="person-charts-container",
        children=[
            html.Div(id="person-time-histogram-container"),
            html.Div(id="person-hour-histogram-container"),
            html.Div(id="person-wordclouds-container")
        ]
    )
])

tab3_layout = html.Div([
    html.H2("Data of a group conversation thread"),

    html.Div(id="groups-output",
             children=[
                 html.Div(id="group-most-messages-container")
             ])
])


# MAIN APP FUNCTIONALITY

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.config.suppress_callback_exceptions = True

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    dbc.Tabs(id="tabs", active_tab="tab1", children=[
                        dbc.Tab(label="Your summary", tab_id="tab1"),
                        dbc.Tab(label="People", tab_id="tab2", children=[
                                html.P("Select a person:"),
                                dcc.Dropdown(
                                    id="person-dropdown",
                                    options=[{"label": str(name), "value": str(name)} for name in df.loc[df["thread_type"] == "Regular"].thread_name.unique()])
                                ]),
                        dbc.Tab(label="Groups", tab_id="tab3", children=[
                            html.P("Select a group:"),
                            dcc.Dropdown(id="group-dropdown",
                                         options=[{"label": name, "value": name} for name in df.loc[df["thread_type"] == "RegularGroup"].thread_name.unique()])
                        ])
                    ])
                )
            ), md=3
        ),
        dbc.Col(
            dbc.Card(
                html.Div(id="content",  className="pt-4 px-4")
            ), md=9, className="overflow-auto"
        )
    ])


], fluid=True, className="pt-4")

# CALLBACKS

# General tab selection callback


@app.callback(Output("content", "children"), Input("tabs", "active_tab"))
def render_content(tab):
    if tab == "tab1":
        return tab1_layout
    elif tab == "tab2":
        return tab2_layout
    else:
        return tab3_layout


# Second tab callbacks
@app.callback(Output("person-time-histogram-container", "children"), Input("person-dropdown", "value"))
def personTimeHistogram(person):
    if person:
        df_slice = df.loc[df["thread_name"] == person]

        personTimeHistogram = px.histogram(df_slice, x="date", color="author")
        personTimeHistogram.update_yaxes(title_text="Number of messages")
        personTimeHistogram.update_xaxes(title_text="Date")
        # personTimeHistogram.update_xaxes(title_text="Date",
        #                                  autorange=True,
        #                                  range=["2014-10-29 18:36:37.3129", "2021-01-05 05:23:22.6871"],
        #                                  rangeslider=dict(
        #                                  autorange=True,
        #                                  range=["2014-10-29 18:36:37.3129", "2021-01-05 05:23:22.6871"]
        #                                  ),
        #                                  type="date")
        personTimeHistogram.update_layout(hovermode="x")
        personTimeHistogram.update_traces(
            hovertemplate='Number of messages: %{y}')
        return dcc.Graph(
            id="person-histogram",
            figure=personTimeHistogram
        )


@app.callback(Output("person-hour-histogram-container", "children"), Input("person-dropdown", "value"))
def personHourHistogram(person):
    if person:
        df_slice = df.loc[df["thread_name"] == person]
        personHourHistogram = px.histogram(df_slice, x="hour", color="author", range_x=[-0.5, 23.5], nbins=24, title="Breakdown of messages sent by hour", color_discrete_sequence=[
            "#264653", "#2a9d8f"], labels={"author": "Author of the message"})
        personHourHistogram.update_yaxes(title_text="Number of messages")
        personHourHistogram.update_xaxes(
            title_text="Hour of day", nticks=24, tickmode='linear', tick0=0.0, dtick=1.0)
        personHourHistogram.update_layout(bargap=0.1, hovermode="x")
        personHourHistogram.update_traces(
            hovertemplate='Number of messages: %{y}')

        return dcc.Graph(
            id="person-hour-histogram",
            figure=personHourHistogram
        )

# this is a mess but we'll have to live with it for now


@app.callback(Output("person-wordclouds-container", "children"), Input("person-dropdown", "value"))
def personWordclouds(person):
    if person:
        yourWordcloud = generateWordCloudImage(person, True)
        theirWordcloud = generateWordCloudImage(person, False)

        return html.Div(id="wordcloud-container",
                        children=html.Div(
                            children=[
                                html.Div(
                                    children=[
                                        html.H2(
                                            children=["Your wordcloud"]),
                                        html.Img(src=yourWordcloud, style={
                                            "display": "block", "width": "100%"})
                                    ],
                                    style={"display": "inline-block", "marginLeft": "auto",
                                           "marginRight": "auto", "width": "40%", "paddingRight": "3%"}
                                ),
                                html.Div(
                                    children=[
                                        html.H2(
                                            children=["Their wordcloud"]),
                                        html.Img(src=theirWordcloud, style={
                                            "display": "block", "width": "100%"})
                                    ],
                                    style={"display": "inline-block", "marginLeft": "auto",
                                           "marginRight": "auto", "width": "40%", "paddingLeft": "3%"}
                                )

                            ],
                            style={"textAlign": "center"}
                        )
                        )


# third tab callbacks

@app.callback(Output("group-most-messages-container", "children"), Input("group-dropdown", "value"))
def groupMostMessages(thread):
    if thread:
        df_sl = df.loc[df["thread_name"] == thread]
        top = df_sl.groupby(["author"]).size(
        ).sort_values(ascending=False).head(10)
        neww = pd.DataFrame()
        neww["count"] = top
        neww["author"] = top.index

        mostMessagesHistogram = px.bar(
            y=neww["author"], x=neww["count"], orientation="h")
        mostMessagesHistogram.update_yaxes(categoryorder="total ascending")

        return dcc.Graph(id="mostMessages",
                         figure=mostMessagesHistogram
                         )


if __name__ == "__main__":
    app.run_server(debug=True)
