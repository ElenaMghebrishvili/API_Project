#საჭირო მოდულების დაიმპორტირება
from win10toast import ToastNotifier
import requests
from jokeapi import Jokes
import asyncio
import json
import sqlite3


DB = 'database.db'
#ვაგზავნით რექვესთს jokeapi-ზე
responce = requests.get('https://v2.jokeapi.dev/joke/Any')

#headers
headers = responce.headers
print(headers)

def print_json(obj):
    print(json.dumps(obj, indent=4))



#status code
status_code = responce.status_code
print("status code: ", status_code)

#ამ კოდის საშუალებით იბეჭდება რენდომ joke მხოლოდ და მხოლოდ 'programming' კატეგორიიდან
async def print_joke_by_category():
    j = await Jokes()  # Initialise the class
    joke = await j.get_joke(category=['programming'])
    if joke["type"] == "single": # Print the joke
        print(joke["joke"])
    else:
        print(joke["setup"])
        print(joke["delivery"])

asyncio.run(print_joke_by_category())


# res მივანიჭოთ api-დან მიღებული json ფორმატის პასუხის მნიშვნელობა
res = {
    "category": "Programming",
    "type": "single",
    "joke": "Why do programmers prefer dark mode? Because light attracts bugs!",
    "flags": {
        "nsfw": False,
        "religious": False,
        "political": False,
        "racist": False,
        "sexist": False,
        "explicit": False
    },
    "id": 42,
    "safe": True,
    "lang": "en"
}

#ფაილის სახელის შექმნა
file_path = 'data.json'

# ჩავწეროთ JSON მონაცემები ფაილში
with open(file_path, 'w') as file:
    json.dump(res, file, indent=4)

#json ობიექტთან სამუშაო ფუნქციების გამოყენებით დავბეჭდოთ რა კატეგორიის ხუმრობაა
category = res['category']
print('კატეგორია: ', category)


#ამ კოდის საშუალებით ბაზაში შევინახავთ იმ ხუმრობებს, რომელთა კატეგორიაა 'programming'
async def print_joke_by_category():
    # დავუკავშირდეთ sqlite3-ის ბაზას
    conn = sqlite3.connect('jokes.db')
    c = conn.cursor()

    # შევქმნათ ხუმრობების ცხრილი თუ უკვე არ არსებობს
    c.execute('''CREATE TABLE IF NOT EXISTS jokes
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 category TEXT,
                 type TEXT,
                 setup TEXT,
                 delivery TEXT,
                 joke TEXT)''')

    j = await Jokes()  # მოვახდინოთ კლასის ინიციალიზება
    joke = await j.get_joke(category=['programming'])

    # შევინახოთ ხუმრობა მონაცემთა ბაზაში
    if joke["type"] == "single":
        c.execute("INSERT INTO jokes (category, type, joke) VALUES (?, ?, ?)",
                  (joke["category"], joke["type"], joke["joke"]))
    else:
        c.execute("INSERT INTO jokes (category, type, setup, delivery) VALUES (?, ?, ?, ?)",
                  (joke["category"], joke["type"], joke["setup"], joke["delivery"]))

    # შევინახოთ ცვლილებები და გავწყვიტოთ მონაცემთა ბაზასთან კავშირი
    conn.commit()
    conn.close()

    # დავბეჭდოთ ხუმრობა
    if joke["type"] == "single":
        print(joke["joke"])
    else:
        print(joke["setup"])
        print(joke["delivery"])


asyncio.run(print_joke_by_category())



#ამ კოდის საშუალებით ეკრანზე შეტყობინების სახით გამოჩნდება ის ხუმრობები, რომლის კატეგორიაა 'programming'

toaster = ToastNotifier()
async def print_joke_by_category():
    j = await Jokes()
    joke = await j.get_joke(category=['programming'])
    if joke["type"] == "single":
        joke_text = joke["joke"]
    else:
        joke_text = f"{joke['setup']}\n{joke['delivery']}"
    toaster.show_toast("Category Joke", joke_text, duration=10)

asyncio.run(print_joke_by_category())