import os
import json
import datetime
import pandas as pd

root = "./messages/inbox"
message_id = 1
output = []
owner = ""


for thread in os.listdir(root):
    for messagefile in os.listdir(os.path.join(root, thread)):
        if (messagefile.endswith("json")):
            filepath = os.path.join(root,thread, messagefile)
            with open(filepath) as jsonfile:
                data = json.load(jsonfile)
                numberofpeople = len(data["participants"])
                threadtype =  data["thread_type"].encode('iso-8859-1').decode('utf-8')
                threadname = data['title'].encode('iso-8859-1').decode('utf-8')
                messages = data["messages"]
                if owner == "" and data["thread_type"] == "Regular" and len(data["participants"])>1:
                    owner = data["participants"][1]["name"].encode('iso-8859-1').decode('utf-8')
                for message in messages:
                    if (message["type"] == "Generic"):
                        author = message["sender_name"].encode('iso-8859-1').decode('utf-8')
                        dt = datetime.datetime.fromtimestamp(message["timestamp_ms"]//1000)
                        whole_date = dt.isoformat()
                        year = dt.year
                        month = dt.month
                        day = dt.day
                        hour = dt.hour
                        minute = dt.minute
                        second = dt.second
                        chars = 0
                        words = 0
                        content = message.get("content")
                        if content:
                            enc = content.encode('iso-8859-1').decode('utf-8')
                            chars = len(content)
                            words = len(content.split(" "))
                        output.append([message_id, threadtype, numberofpeople, threadname, author, whole_date, year, month, day, hour, minute, second, chars, words, enc])
                        message_id+=1

df = pd.DataFrame(output, columns=["id", "thread_type", "number_of_people", "thread_name", "author", "date", "year", "month", "day", "hour", "minute", "second", "chars", "words", "content"])

with open("owner.txt", "w", encoding="utf-8") as ownerfile:
    ownerfile.write(owner)


print(df.head())

df.to_csv("messages.csv", index=False)
print(str(len(df))+ " wiadomości")




