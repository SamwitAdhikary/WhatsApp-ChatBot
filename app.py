from flask import Flask, request
import requests
from twilio.twiml.messaging_response import MessagingResponse
import wikipediaapi
import randfacts
import random
from flask import Flask, request, jsonify, Response


# List of trivia questions and answers


app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World!"

@app.route("/sms", methods=["POST"])
def sms():
    incoming_msg = request.values.get('Body', '').lower()
    resp = MessagingResponse()
    msg = resp.message()

    if 'good morning' in incoming_msg:
        #! Return a gesture good morning
        msg.body('Good Morning..\nHave a nice day..')

    elif 'good afternoon' in incoming_msg:
        #! Return a gesture good morning
        msg.body('Good Afternoon..')

    elif 'good evening' in incoming_msg:
        #! Return a gesture good evening
        msg.body('Good Evening..\nHow was your day today?')

    elif 'good night' in incoming_msg:
        #! Return a good night gesture
        msg.body('Good Night..\nSee you tomorrow..')

    elif 'fine' in incoming_msg:
        #! Return a sweet gesture and ask what to do
        msg.body('Nice to hear that..\nWhat can I do for you master?')

    elif 'who made you' in incoming_msg:
        #! Telling about your developer
        msg.body('Samwit Adhikary made me.❤️❤️')

    elif "who are you" in incoming_msg:
        #! Telling who am I
        msg.body('I am called Whatsapp Bot made by Samwit Adhikary.❤️❤️')

    elif 'who developed you' in incoming_msg:
        #! Returning whatsapp obeying
        msg.body('I obey whatsapp messenger.')

    elif 'how are you' in incoming_msg:
        #! Telling how am I
        msg.body('I am fine..\nWhat about you??')

    elif '#about' in incoming_msg:
        #! Telling your features
        msg.body("Hi! I am Whatsapp Bot made By Samwit Adhikary. Did you know that you can find out the weather, a movie rating and much more on whatsapp with just a few words!\nTry one of the following and I'll look it up for you!\n\n#weather PLACE: Check out the weather at any place.\n\n#wiki NAME: Search Wikipedia for anything you want.\n\n#quote: We'll send you awesome quote whenever you want it.\n\n#movie NAME: Checkout the IMDB Rating about any movie.\n\n#book NAME: Get details of any book you're interested in.\n\n#meaning WORD: Don't know the meaning of a word someone just messaged you? Try out my built in dictionary\n\n#synonym WORD: Don't know the synonyms of any word. Try my built in synonym finder.\n\n#coronastats: To get current status of Coronavirus in India\n\n#fact: Awesome facts, served streaming hot, whenever you want it!\n\n#news: Get the top 5 breaking news.\n\n#joke: Get jokes.")

    elif '#joke' in incoming_msg:
        #! Return random joke.
        url = 'https://official-joke-api.appspot.com/jokes/general/random'
        r = requests.get(url)
        rj = r.json()
        try:
            for joke in rj:
                setup = joke['setup']
                punch = joke['punchline']
                msg.body(f'{setup}\n{punch}')
        except:
            msg.body('Sorry.. No Joke Found!!')

    elif '#news' in incoming_msg:
        #! Return top 5 headlines.
        url = 'http://newsapi.org/v2/top-headlines?country=in&apiKey=<Your Api Key>'
        r = requests.get(url)
        rj = r.json()
        try:
            articles = rj['articles']
            for news in articles[:5]:
                title = news['title']
                link = news['url']
                msg.body(f"\nTitle: {title}\n{link}\n")
        except:
            msg.body('Sorry.. No News Found!!')

    elif '#fact' in incoming_msg:
        #! Return interesting facts.
        try:
            facts = randfacts.getFact()
            msg.body(facts)
        except:
            msg.body('Sorry.. No Facts Found!!')

    elif '#coronastats' in incoming_msg:
        #! Return covid19 stats.
        url = 'https://coronavirus-19-api.herokuapp.com/countries/india'
        r = requests.get(url)
        rj = r.json()
        try:
            totalCases = rj['cases']
            totalRecovered = rj['recovered']
            totalDeaths = rj['deaths']
            active = rj['active']
            critical = rj['critical']
            todaysCases = rj['todayCases']
            todaysDeaths = rj['todayDeaths']
            msg.body(f"The current stats for COVID-19 in India are as follow:\n\nTotal Cases: {totalCases}\nTotal Recovered: {totalRecovered}\nTotal Deaths: {totalDeaths}\nActive Cases: {active}\nCritical Cases: {critical}\nNew Cases Today: {todaysCases}\nNew Deaths: {todaysDeaths}\n\nYou can get the latest stats by sending #coronastats")
        except:
            msg.body('Sorry I am unable to retrive corona stats at this time, try later.')

    elif "#synonym" in incoming_msg:
        #! Return 10 synonyms of the word.
        word = incoming_msg.replace('#synonym ', '')
        url = f'https://api.dictionaryapi.dev/api/v2/entries/en/{word}'
        r = requests.get(url)
        synonym = []
        rj = r.json()
        try:
            for i in rj:
                s = i['meanings']
                for j in s:
                    y = j['definitions']
                    for k in y:
                        try:
                            n = k['synonyms']
                            for syn in n:
                                synonym.append(syn)
                        except:
                            pass
        except:
            synonym.append('Sorry.. No Word Found!!')

        msg.body('Synonyms: \n\n')
        for mean in synonym[:10]:
            msg.body(mean + ', ')

    elif '#meaning' in incoming_msg:
        #! Return meaning of word.
        word = incoming_msg.replace('#meaning ', '')
        url = f'https://api.dictionaryapi.dev/api/v2/entries/en/{word}'

        examples = []
        defs = []
        try:
            r = requests.get(url)
            rj = r.json()

            for data in rj:
                meaning = data['meanings']
                for data1 in meaning:
                    definitions = data1['definitions']
                    for data2 in definitions:
                        # print(data2)
                        definition = data2['definition']
                        defs.append(definition)
                        try:

                            example = data2['example']
                            examples.append(example)
                        except:
                            pass
            msg.body('*Meaning:*\n')
            for i in defs:
                msg.body(i + ',\n')
            msg.body('*Examples:*\n')
            for j in examples:
                msg.body(j + ', ')
        except:
            msg.body('Sorry.. No Words Found!!')

    elif '#book' in incoming_msg:
        #! Return book details
        name = incoming_msg.replace('#book ', '')
        url = f'https://www.googleapis.com/books/v1/volumes?q={name}'
        r = requests.get(url)
        try:
            rj = r.json()
            top = rj['items']
            vinfo = []
            for i in top:
                for j in i:
                    if(j=='volumeInfo'):
                        vinfo.append(i[j])
            bTitle = []
            subtitle = []
            author = []
            bRating = []
            publisher = []
            buylink = []

            for i in vinfo:
                for j in i:
                    try:
                        if j == 'title':
                            bTitle.append(i[j])
                        elif j == 'subtitle':
                            subtitle.append(i[j])
                        elif j == 'authors':
                            author.append(i[j])
                        elif j == 'averageRating':
                            bRating.append(i[j])
                        elif j == 'publisher':
                            publisher.append(i[j])
                        elif j =='canonicalVolumeLink':
                            buylink.append(i[j])
                    except:
                        if j == 'title':
                            bTitle.append(i[j])
                        elif j == 'authors':
                            author.append(i[j])
                        elif j == 'averageRating':
                            bRating.append(i[j])
                        elif j == 'publisher':
                            publisher.append(i[j])
                        elif j =='canonicalVolumeLink':
                            buylink.append(i[j])

            try:
                msg.body(f"Title: {bTitle[0]}\nSubtitle: {subtitle[0]}\nAuthor: {author[0][0]}\nRating: {bRating[0]}\nPublisher: {publisher[0]}\n\n{buylink[0]}")
            except:
                msg.body(f"Title: {bTitle[0]}\nAuthor: {author[0][0]}Rating: {bRating[0]}\nPublisher: {publisher[0]}\n\n{buylink[0]}")
        except:
            msg.body(f"Sorry.. Can't find book {name}..\nTry some other book.")



    elif '#movie' in incoming_msg:
        name = incoming_msg.replace('#movie ', '')
        ids = []
        try:
            try:
                url = f'http://www.omdbapi.com/?s={name}&apikey=<Your Api Key>'
                r = requests.get(url)
                rj = r.json()
                search = rj['Search']
                for data in search:
                    ID = data['imdbID']
                    ids.append(ID)
            except:
                url = f'https://imdb-api.com/en/API/SearchAll/k_4livlpf2/{name}'
                r = requests.get(url)
                rj = r.json()
                results = rj['results']
                for data in results:
                    ID = data['id']
                    ids.append(ID)
            iD = ids[0]

            url2 = f'http://www.omdbapi.com/?i={iD}&apikey=<Your Api Key>'
            req = requests.get(url2)
            rjson = req.json()
            title = rjson['Title']
            year = rjson['Year']
            release = rjson['Released']
            rtime = rjson['Runtime']
            actor = rjson['Actors']
            lang = rjson['Language']
            rating = rjson['imdbRating']
            genre = rjson['Genre']
            poster = rjson['Poster']

            msg.body(f'Movie Info:\n\nTitle: {title}({year})\nReleased: {release}\nRating: {rating}\nRuntime: {rtime}\nLanguage: {lang}\nGenre: {genre}\nActors: {actor}\n\nPoster:\n{poster}')
        except:
            msg.body(f"Sorry can't find movie {name}")


    elif '#weather' in incoming_msg:
        #! Returning Weather Report
        city_name = incoming_msg.replace('#weather ', '')
        r = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid=<Your Api Key>&units=metric')
        try:
            data = r.json()
            name = data['name']
            feels_like = data['main']['feels_like']
            humidity = data['main']['humidity']
            latitude = data['coord']['lat']
            longitude = data['coord']['lon']
            country = data['sys']['country']
            temp = data['main']['temp']
            wind_speed = data['wind']['speed']
            msg.body(f"City Name: {name} - {country}\nLongitude: {longitude}°\nLatitude: {latitude}°\nFeels Like: {feels_like}°C\nTemperature: {temp}°C\nHumidity: {humidity}%\nWind Speed: {wind_speed}m/s")
        except:
            titleName = city_name.title()
            msg.body(f"Sorry.. Can't find *{titleName}*..\nEnter any city name..\n*#weather kolkata*")

    elif '#wiki' in incoming_msg:
        #! Returning summary from wikipedia
        query = incoming_msg.replace('#wiki ', '')
        wiki = wikipediaapi.Wikipedia('en')
        try:
            page = wiki.page(query)
            url = page.fullurl
            summary = page.summary[0:1500]
            msg.body(f'According to wikipedia..\n\n{summary}...\n{url}')
        except:
            msg.body("Sorry can't find anything.\nTry another search..")

    elif '#quote' in incoming_msg:
        #! Returning quotes
        r = requests.get('http://api.quotable.io/random')
        if r.status_code == 200:
            data = r.json()
            quote = f'{data["content"]} ({data["author"]})'
        else:
            quote = 'Sorry I am unable to retrive quote at this time, try later.'
        msg.body(quote)
    
    #-->feature which asking Python interview preparation questions
    elif '#trivia' in incoming_msg:
        trivia_questions = [
            {"question": "What is the difference between `deepcopy` and `shallowcopy` in Python?"},
            {"question": "Explain the difference between `list` and `tuple` in Python."},
            {"question": "What is a lambda function in Python, and when would you use it?"},
            {"question": "How does Python's garbage collection work?"},
            {"question": "What is the purpose of the `self` keyword in Python classes?"},
            {"question": "How do you handle exceptions in Python?"},
            {"question": "What is the Global Interpreter Lock (GIL) in Python?"},
            {"question": "Explain the use of decorators in Python with an example."},
            {"question": "What are Python generators, and how do they differ from iterators?"},
            {"question": "What are list comprehensions in Python, and why are they useful?"},
            {"question": "Explain the difference between `__init__` and `__new__` in Python classes."},
            {"question": "How do you implement method overloading in Python?"},
            {"question": "What are metaclasses in Python, and how do they work?"},
            {"question": "What is the difference between `==` and `is` in Python?"},
            {"question": "How would you reverse a string in Python?"}
        ]
        # Select a random trivia question
        trivia = random.choice(trivia_questions)
        question = trivia["question"]
        # Send the trivia question
        msg.body(f"Trivia Question: {question}")


    
    else:
        msg.body("Sorry.. I didn't get that..\nTry *#about* ")

    return str(resp)
    

if __name__ == "__main__":
    app.run(debug=True)


