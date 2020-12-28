import pandas as pd
from wordcloud import WordCloud


df = pd.read_csv("messages.csv")

filt = df.loc[df["author"]=="Mikołaj Spytek"]

text = filt.content.str.cat(sep=" ")

wc = WordCloud(width=1200, height=600, background_color="rgba(255, 255, 255, 0)", mode="RGBA").generate(text)

image = wc.to_image()
image.show()

print(type(image))