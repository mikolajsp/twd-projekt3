import dash
import os
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

#https://github.com/fergiemcdowall/stopword

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

basefile = os.path.dirname(os.path.abspath(__file__))
owfile = os.path.join(basefile, "owner.txt")

with open(owfile, mode="r", encoding="utf-8") as ownerfile:
    owner = ownerfile.read()


def turn(val, owner):
    if val == owner:
        return "You"
    else:
        return "Someone else"

messagefile = os.path.join(basefile, "messages.csv")

# Reactions dataframe
reactionfile = os.path.join(basefile, "reactions.csv")
df_reactions = pd.read_csv(reactionfile)
df_reactions["who"] = df_reactions["reacting_person"].apply(turn, args=(owner,))

df = pd.read_csv(messagefile)
df["who"] = df["author"].apply(turn, args=(owner,))

fig_1 = px.histogram(df, x="date", color="who", title="Your messages over time", labels={
                     "date": "Date", "who": "Who sent the message"})
fig_1.update_yaxes(title_text="Number of messages")


fig_2 = px.histogram(df, x="hour", color="who", range_x=[0, 23], nbins=24, title="Breakdown of messages sent by hour", color_discrete_sequence=[
                     "#264653", "#2a9d8f"], labels={"who": "Who sent the message"})
fig_2.update_yaxes(title_text="Number of messages")
fig_2.update_xaxes(title_text="Hour of day", nticks=24)
fig_2.update_layout(bargap=0.1)


tab1_layout = html.Div([
    html.H2("Overview of your data"),
    dcc.Graph(
        id="default-histogram",
        figure=fig_1),
    dcc.Graph(
        id="hour-histogram",
        figure=fig_2
    )
])

tab2_layout = html.Div([
    dcc.Dropdown(
        id="person-dropdown",
        options = [{"label": name, "value": name} for name in df.loc[df["thread_type"] == "Regular"].thread_name.unique()]),
    html.Div(
        id="person-histogram-container"
    )
])

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.config.suppress_callback_exceptions = True

app.layout = html.Div([
    dcc.Tabs(id="tabs", value="tab1", children=[
        dcc.Tab(label="Your summary", value="tab1"),
        dcc.Tab(label="People", value="tab2"),
        dcc.Tab(label="Groups", value="tab3")
    ]),
    html.Div(id="content")
])


# @app.callback(Output("person-dropdown", "options"), [Input("tabs", "value")])
# def fill_dropdown(tab):
#     lis = df.loc[df["thread_type"] == "Regular"].thread_name.unique()
#     opts = [{"label": name, "value": name} for name in lis]
#     return opts


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
    retlist = []
    if person:
        df_slice = df.loc[df["thread_name"] == person]

        # prepare first histogram
        person_plot = px.histogram(df_slice, x="date", color="author")
        person_plot.update_yaxes(title_text="Number of messages")
        person_plot.update_xaxes(title_text="Date")

        retlist.append(
            dcc.Graph(
                id="person-histogram",
                figure=person_plot
            )
        )

        # prepare second histogram
        hour_plot = px.histogram(df_slice, x="hour", color="author", range_x=[0, 23], nbins=24, title="Breakdown of messages sent by hour", color_discrete_sequence=[
                                 "#264653", "#2a9d8f"], labels={"author": "Author of the message"})
        hour_plot.update_yaxes(title_text="Number of messages")
        hour_plot.update_xaxes(title_text="Hour of day", nticks=24)
        hour_plot.update_layout(bargap=0.1)

        retlist.append(
            dcc.Graph(
                id="person-hour-histogram",
                figure=hour_plot
            )
        )

        # prepare wordclouds
        yourtext = df_slice.loc[df_slice["author"]== owner].content.str.cat(sep=" ")
        

        theirtext = df_slice.loc[df_slice["author"]!= owner].content.str.cat(sep=" ")
        

        if len(yourtext) >0 and len(theirtext) >0:
            yourwc = WordCloud(
            width=1200, height=600, background_color="rgba(255, 255, 255, 0)", mode="RGBA", stopwords=stop_words).generate(yourtext)
            yourwcimg = yourwc.to_image()
            theirwc = WordCloud(
            width=1200, height=600, background_color="rgba(255, 255, 255, 0)", mode="RGBA", stopwords=stop_words).generate(theirtext)
            theirwcimg = theirwc.to_image()
            retlist.append(html.Div(id="wordcloud-container",
                                    children=html.Div(
                                        children=[
                                            html.Div(
                                                children=[
                                                    html.H2(
                                                        children=["Your wordcloud"]),
                                                    html.Img(src=yourwcimg, style={
                                                        "display": "block", "width": "100%"})
                                                ],
                                                style={"display": "inline-block", "marginLeft": "auto",
                                                       "marginRight": "auto", "width": "40%", "paddingRight": "3%"}
                                            ),
                                            html.Div(
                                                children=[
                                                    html.H2(
                                                        children=["Their wordcloud"]),
                                                    html.Img(src=theirwcimg, style={
                                                        "display": "block", "width": "100%"})
                                                ],
                                                style={"display": "inline-block", "marginLeft": "auto",
                                                       "marginRight": "auto", "width": "40%", "paddingLeft": "3%"}
                                            )

                                        ],
                                        style={"textAlign": "center"}
                                    )
                                    ))
    return retlist

if __name__ == "__main__":
    app.run_server(debug=True)
