import kivy
import requests
import json
import urllib.request
import play_scraper
import collections
import pandas as pd
import matplotlib
# matplotlib.use('module://kivy.garden.matplotlib.backend_kivy')
import matplotlib.pyplot as plt
import seaborn as sb
# import re
import io
import kivy.uix.widget

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.button import ButtonBehavior
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import AsyncImage, Image, CoreImage
from kivy.uix.scrollview import ScrollView
from kivy.uix.actionbar import ActionBar
from kivy.uix.actionbar import ActionView
from kivy.uix.actionbar import ActionItem
from kivy.uix.actionbar import ActionPrevious
from kivy.properties import VariableListProperty
from kivy.properties import StringProperty
from kivy.core.window import Window
from kivy.core.text import LabelBase
from kivy.graphics import Color, Rectangle
from kivy.config import Config
from kivy.base import runTouchApp
from kivy.factory import Factory as fact
from bs4 import BeautifulSoup
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
from functools import partial
from google_play_scraper import Sort, reviews, reviews_all
# from textblob import TextBlob
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
# from kivy_garden.graph import Graph
from PIL import Image

Config.set('graphics', 'resizable', True)

kivy.require("2.0.0")

LabelBase.register(name="Sonorous", fn_regular="Sonorous.otf")
LabelBase.register(name="NotoSansJP", fn_regular="NotoSansJP-Regular.otf")

class MainPage(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        # self.horbox = BoxLayout(orientation="vertical")
        # self.add_widget(self.horbox)

        self.box1 = BoxLayout(orientation="horizontal", padding=[50, 50, 50, 0])
        self.add_widget(self.box1)
        self.lbl = Label(text='APP:RE', halign='center', font_name="Sonorous", font_size="50sp", valign='bottom')
        self.box1.add_widget(self.lbl)

        # self.horbox = BoxLayout(orientation="vertical")
        # self.add_widget(self.horbox)
        #
        # self.horbox = BoxLayout(orientation="vertical")
        # self.add_widget(self.horbox)

        # self.verbox1 = BoxLayout(orientation="vertical")
        # self.horbox.add_widget(self.verbox1)

        # self.verbox2 = BoxLayout(orientation="vertical")
        # self.add_widget(self.verbox2)

        # self.verbox3 = BoxLayout(orientation="vertical")
        # self.horbox.add_widget(self.verbox3)
        self.box2 = BoxLayout(orientation="horizontal", padding=[40, 0, 40, 70])
        self.add_widget(self.box2)
        self.btn = Button(background_normal="circle.png", border=(0,0,0,0), text="Search", font_size="20sp", font_name="NotoSansJP", size_hint_x=.2)
        self.btn.bind(on_press=self.search_button)
        self.box2.add_widget(self.btn)



        # self.horbox = BoxLayout(orientation="horizontal")
        # self.add_widget(self.horbox)
        # self.smallhorbox1 = BoxLayout(orientation="horizontal")
        # self.verbox2.add_widget(self.smallhorbox1)
        # self.smallhorbox2 = BoxLayout(orientation="horizontal")
        # self.verbox2.add_widget(self.smallhorbox2)


    def search_button(self, event):
        sentimento.screen_manager.transition.direction = "left"
        sentimento.screen_manager.current = "Search"

class SearchPage(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1

        # actionbar = ActionBar(pos_hint={'top': 1})
        # av = ActionView()
        # prev = ActionPrevious(title='', with_previous=True)
        # prev.bind(on_release=self.back_button)
        # av.add_widget(prev)
        # # txtinput = TextInput(multiline=False)
        # # av.add_widget(txtinput)
        # # av.add_widget(fact.ActionOverflow())
        # actionbar.add_widget(av)
        # self.add_widget(actionbar)

        self.box = BoxLayout(orientation="horizontal", padding=[10], spacing=10)
        self.add_widget(self.box)
        self.backbtn = Button(background_normal="arrow.png", size_hint_x=.2, border=(0,0,0,0))
        self.backbtn.bind(on_press=self.back_button)
        self.box.add_widget(self.backbtn)
        self.txtinput = TextInput(multiline=False, halign='left', font_size="15sp", font_name="NotoSansJP")
        self.txtinput.bind(text = self.suggest)
        # self.txtinput.bind(on_text_validate = self.suggest(self.txtinput.text))
        self.box.add_widget(self.txtinput)
        self.srchbtn = Button(background_normal="search.png", size_hint_x=.2, border=(0,0,0,0))
        self.srchbtn.bind(on_press=self.search_button)
        self.box.add_widget(self.srchbtn)
        self.dict = {}
        self.btn = []
        self.press = []
        self.count = 0

        for i in range(0, 10):
            self.btn.append(Button(text="", halign="left", background_color=(0, 0, 0, 0)))
            self.add_widget(self.btn[i])

    def suggest(self, event, text):

        if self.txtinput.text == "":
            for i in range(0, 10):
                self.btn[i].text = ""
        else:
            # self.url = "https://rapidapi.p.rapidapi.com/autocomplete"
            # self.querystr = {"store":"google","term":self.txtinput.text,"language":"en"}
            # self.headers = {
            #     'x-rapidapi-host': "app-stores.p.rapidapi.com",
            #     'x-rapidapi-key': "YOUR-API-KEY"
            # }
            # self.response = requests.request("GET", self.url, headers=self.headers, params=self.querystr)
            # self.lst = json.loads(self.response.text)
            self.lst = play_scraper.suggestions(self.txtinput.text)

            if self.count > 0:
                for i in range(0, len(self.lst)):
                    self.btn[i].unbind(on_press=self.press[i])
                self.press.clear()

            for i in range(0, len(self.lst)):
                self.btn[i].text = self.lst[i]
                self.btn[i].font_name= "NotoSansJP"
                # if self.isbound(self.select_sug) == True:
                self.press.append(lambda *args, _id=self.btn[i].text: self.select_sug(_id, *args))
                self.btn[i].bind(on_press=self.press[i])
            self.count = self.count + 1
    # def isbound(self, method):
    #     return method.im_self is not None

    def select_sug(self, sug, event):
        self.txtinput.text = sug
        for i in range(0, 10):
            self.btn[i].text = ""

        # if self.txtinput.text == "":
        #     for i in range(0, 10):
        #         self.lbl = Label(text="")
        #         self.add_widget(self.lbl)
        # else:
        #     for i in range(0, len(self.lst)-1):
        #         self.lbl = Label(text=self.lst[i])
        #         self.add_widget(self.lbl)
        #     for j in range(0, 10-len(self.lst)):
        #         self.lbl = Label(text="")
        #         self.add_widget(self.lbl)

    def back_button(self, event):
        sentimento.screen_manager.transition.direction = "right"
        sentimento.screen_manager.current = "Main"

    def search_button(self, event):
        # self.url = "https://rapidapi.p.rapidapi.com/search"
        # self.querystr = {"store": "google", "term": self.txtinput.text, "language": "en"}
        # self.headers = {
        #     'x-rapidapi-host': "app-stores.p.rapidapi.com",
        #     'x-rapidapi-key': "YOUR-API-KEY"
        # }
        # self.response = requests.request("GET", self.url, headers=self.headers, params=self.querystr)
        # self.dict = json.loads(self.response.text)
        if self.txtinput.text != "":
            self.dict = play_scraper.search(self.txtinput.text, gl="my", detailed=True)
            sentimento.result_page.dictlist(self.dict)
            sentimento.screen_manager.transition.direction = "left"
            sentimento.screen_manager.current = "Result"

class ResultPage(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.box = BoxLayout(orientation="horizontal", padding=[10], spacing=10, size_hint_y=None, height=60)
        self.add_widget(self.box)
        self.backbtn = Button(background_normal="arrow.png", size_hint=(None, None), width=40, height=40, border=(0,0,0,0))
        self.backbtn.bind(on_press=self.back_button)
        self.box.add_widget(self.backbtn)
        self.scrl = ScrollView(size=(Window.width, Window.height))
        self.add_widget(self.scrl)
        self.grid = GridLayout(cols=2, size_hint_y=None, spacing=10)
        self.grid.bind(minimum_height=self.grid.setter('height'))
        self.scrl.add_widget(self.grid)

    def back_button(self, event):
        self.clear_widgets()
        sentimento.screen_manager.transition.direction = "right"
        sentimento.screen_manager.current = "Search"

    def dictlist(self, mydict):
        # self.id = []
        # self.img = []
        # self.name = []
        # self.imgbtn = []
        # self.txtbtn = []
        # for i in range(0, len(mydict)-1):
        #     self.id.append(mydict[i].get("id"))
        #     self.img.append(mydict[i].get("icons").get("medium"))
        #     self.name.append(mydict[i].get("name"))
        for i in range(0, len(mydict)):
            self.img = AsyncImage(source=mydict[i].get("icon"), size_hint_x=.5)
            # self.btn = (Button(background_normal=mydict[i].get("icons").get("medium")))
            # self.btn.bind(on_press=lambda *args, _id=mydict[i]: self.select_app(_id, *args))
            self.grid.add_widget(self.img)
            self.btn2 = Button(text=mydict[i].get("title"), text_size=(self.width, None), size_hint=(1, None), background_color=(0,0,0,0))
            self.btn2.bind(on_press=lambda *args, _id=mydict[i]: self.select_app(_id, *args))
            self.grid.add_widget(self.btn2)

    def select_app(self, book, event):
        # self.book = book
        # self.url = "https://rapidapi.p.rapidapi.com/details"
        # self.querystr = {"store":"google","id":self.book.get("id"),"language":"en"}
        # self.headers = {
        #     'x-rapidapi-host': "app-stores.p.rapidapi.com",
        #     'x-rapidapi-key': "YOUR-API-KEY"
        # }
        # self.response = requests.request("GET", self.url, headers=self.headers, params=self.querystr)
        # self.dict = json.loads(self.response.text)
        self.dict = play_scraper.details(book.get("app_id"))

        sentimento.app_page.showdetails(self.dict)
        sentimento.screen_manager.transition.direction = "left"
        sentimento.screen_manager.current = "App"

class AppPage(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.menubox = BoxLayout(orientation="horizontal", padding=[10], spacing=10, size_hint_y=None, height=60)
        self.add_widget(self.menubox)
        self.backbtn = Button(background_normal="arrow.png", size_hint=(None, None), width=40, height=40, border=(0,0,0,0))
        self.backbtn.bind(on_press=self.back_button)
        self.menubox.add_widget(self.backbtn)
        self.scrl = ScrollView(size=(Window.width, Window.height))
        self.add_widget(self.scrl)
        self.box = BoxLayout(orientation="vertical")
        # self.box.bind(minimum_height=self.box.setter('height'))
        self.scrl.add_widget(self.box)
        # self.box = BoxLayout(orientation="vertical", size_hint_y = None)
        # self.box.bind(minimum_height=self.box.setter('height'))
        # self.scrl.add_widget(self.box)
        self.smallbox = BoxLayout(orientation="horizontal")
        # self.smallbox = BoxLayout(orientation="horizontal")
        self.box.add_widget(self.smallbox)

    def back_button(self, event):
        self.clear_widgets()
        sentimento.screen_manager.transition.direction = "right"
        sentimento.screen_manager.current = "Result"

    def showdetails(self, dict):
        self.img = AsyncImage(source=dict.get("icon"), size_hint_x=.5)
        self.smallbox.add_widget(self.img)
        self.verbox = BoxLayout(orientation="vertical")
        self.smallbox.add_widget(self.verbox)
        self.name = Label(text=dict.get("title")+"\n\n"+dict.get("developer"), font_name="NotoSansJP")
        self.verbox.add_widget(self.name)

        # self.devname = Label(text=dict.get("developer"))
        # self.verbox.add_widget(self.devname)

        # self.dtls = {}
        # self.url = "https://rapidapi.p.rapidapi.com/reviews"
        # self.querystr = {"store":"google","id":dict.get("id"),"language":"en"}
        # self.headers = {
        #     'x-rapidapi-host': "app-stores.p.rapidapi.com",
        #     'x-rapidapi-key': "YOUR-API-KEY"
        # }
        # self.response = requests.request("GET", self.url, headers=self.headers, params=self.querystr)
        # print(self.response.text)
        self.result, continuation_token = reviews(
            dict.get("app_id"),
            lang = "en",
            country = "my",
            sort = Sort.MOST_RELEVANT,
            count = 200,
            filter_score_with = None
        )

        # self.dtls = json.loads(self.response.text)
        # review_list = self.data_scrape()

        self.client = language.LanguageServiceClient()
        string_val = ""
        for i in range(0, len(self.result)-1):
            string_val += self.result[i].get("content")
        doc = language.types.Document(content=string_val, type='PLAIN_TEXT')
        response = self.client.analyze_sentiment(document=doc, encoding_type='UTF32')
        sentiment = response.document_sentiment
        # print(sentiment.score)
        # print(sentiment.magnitude)
        self.score_title = Label(text="Rating Score", font_name="Sonorous", halign="center")
        self.box.add_widget(self.score_title)
        self.score = dict.get("score") + " / 5 stars"
        self.lblscore = Label(text=self.score, font_name="NotoSansJP", halign="center")
        self.box.add_widget(self.lblscore)
        self.category = ""
        if sentiment.score == 1:
            self.category = "Perfect!"
        elif sentiment.score >= 0.5 and sentiment.score < 1:
            self.category = "Very positive"
        elif sentiment.score > 0 and sentiment.score < 0.5:
            self.category = "Positive"
        elif sentiment.score == 0:
            self.category = "Neutral"
        elif sentiment.score > -0.5 and sentiment.score < 0:
            self.category = "Negative"
        elif sentiment.score > -1 and sentiment.score < -0.5:
            self.category = "Very negative"
        elif sentiment.score == -1:
            self.category = "You might want to choose another app..."
        self.react = Label(text="Overall sentiment", font_name="Sonorous", halign="center")
        self.box.add_widget(self.react)
        self.lblreact = Label(text=self.category, font_name="NotoSansJP", halign="center")
        self.box.add_widget(self.lblreact)

        self.lst = []
        self.wordcount = {}
        # str = re.sub(r'\b\w{1,2}\b', '', str)
        for each in string_val.lower().split():
            new_each = each.replace("<br/>", "")
            new_each = new_each.replace("&amp;", "")
            new_each = new_each.replace(",", "")
            new_each = new_each.replace(".", "")
            new_each = new_each.replace("*", "")
            new_each = new_each.replace("!", "")
            new_each = new_each.replace(":P", "")
            new_each = new_each.replace(":p", "")
            new_each = new_each.replace("XD", "")
            new_each = new_each.replace("xD", "")
            new_each = new_each.replace("xd", "")
            new_each = new_each.replace("xp", "")
            new_each = new_each.replace(":)", "")
            new_each = new_each.replace(":D", "")
            new_each = new_each.replace(":d", "")
            new_each = new_each.replace(":", "")
            new_each = new_each.replace("\"", "")
            new_each = new_each.replace("â€œ", "")
            new_each = new_each.replace("â€~", "")
            self.lst.append(new_each)

        # for each in range(len(self.lst)):
        #     if len(self.lst[each]) < 3:
        #         self.lst.remove(self.lst[each])

        self.stop_words = stopwords.words('english')
        # self.lst = []
        # for each in range(len(self.worddict)):
        #     self.lst.append(self.worddict)
        self.df = pd.DataFrame(self.lst, columns=['Word'])
        # self.lemmatizer = WordNetLemmatizer()
        # self.new_lst = []
        # for each in range(len(self.lst)):
        #     self.new_lst.append(self.lemmatizer.lemmatize(self.lst[each]))
        # df = pd.DataFrame(self.new_lst, columns=['Word'])
        # df['Word'] = df['Word'].apply(lambda x: [w for w in x.split() if len(w) > 2])
        self.review = [self.remove_stop(r.split()) for r in self.df['Word']]
        print(self.review)
        # for each in range(len(self.review)):
        #     if each == '':
        #         self.review.remove(each)
        self.counter = collections.Counter(self.review)
        self.worddict = self.counter.most_common(11)
        self.new_df = pd.DataFrame(self.worddict, columns = ['Word', 'Count'])
        # print(self.new_df.iloc[1:12])
        self.new_df = self.new_df.drop([0], axis=0)
        # self.new_df = self.new_df.iloc[1:12]
        self.rev_word = self.new_df['Word'].tolist()
        self.rev_count = self.new_df['Count'].tolist()
        self.rev_percent = []
        self.percent = 0
        self.string_value = ""
        self.table_title = Label(text="Top Most Common Word", font_name="Sonorous", halign="center")
        self.box.add_widget(self.table_title)
        self.percent = self.rev_count[0]/len(self.review)*100
        self.string_value = str(round(self.percent, 2))
        self.table_content = Label(text=self.rev_word[0]+" with "+self.string_value+"% occurence", font_name="NotoSansJP", halign="center")
        self.box.add_widget(self.table_content)
        # self.box.add_widget(self.table_title)
        # self.table = GridLayout(cols=2)
        # self.box.add_widget(self.table)
        # self.table_word = Label(text="Word", size_hint_x=0.3, bold=True)
        # self.table_percent = Label(text="Percentage of appearance (%)", bold=True)
        # self.table.add_widget(self.table_word)
        # self.table.add_widget(self.table_percent)
        # for i in range(len(self.rev_count)):
        #     self.percent = self.rev_count[i]/len(self.review)*100
        #     self.string_value = str(round(self.percent, 2))
        #     self.rev_percent.append(self.string_value)
        # for i in range(len(self.rev_word)):
        #     self.word_lbl = Label(text=self.rev_word[i], font_name="NotoSansJP", size_hint_x=0.5)
        #     self.table.add_widget(self.word_lbl)
        #     self.percent_lbl = Label(text=self.rev_percent[i], font_name="NotoSansJP")
        #     self.table.add_widget(self.percent_lbl)

        # d = self.new_df.nlargest(columns="Count", n=10)
        # plt.figure(figsize=(10, 5))
        # axis = sb.barplot(data=d, x="Word", y="Count")
        # axis.set(ylabel = 'Count')
        # plt.show()

        # buf = io.BytesIO()
        # plt.savefig(buf, format='png')
        # buf.seek(0)
        #
        # # im.show()
        # graphbtn = Button(text="See most common keywords")
        # graphbtn.bind(on_press=self.show_graph(buf))
        # self.box.add_widget(graphbtn)

        # df = pd.DataFrame(lst, columns = ['Word', 'Count'])


        # df['Adjectives'] = df['Word'].apply(self.extract_adj)
        # print(type(lst))
        # print(lst)

    # def show_graph(self, buf):
    #     self.im = Image.open(buf)
    #     im.show()
    #     buf.close()

    def remove_stop(self, rev):
        new_rev = " ".join([i for i in rev if i not in self.stop_words])
        return new_rev

    # def extract_adj(self, text):
    #     bb = TextBlob(text)
    #     return [word for (word, tag) in bb.tags if tag.startswith("JJ")]

        # btn = Button(
        #     text = "Submit"
        # )
        # btn.bind(on_press = self.button_pressed)

        # box.add_widget(btn)

    # def data_scrape(self):
    #     url = 'https://www.yelp.com/biz/milk-and-cream-cereal-bar-new-york?osq=Ice+Cream'
    #     ourUrl = urllib.request.urlopen(url) #use request to open the URL
    #
    #     #create a Beautiful Soup object, which represents the doc as a nested data structure
    #     #parse the page
    #     soup = BeautifulSoup(ourUrl, 'html.parser')
    #
    #     review = []
    #     for i in soup.find_all('p', {'class':'lemon--p__373c0__3Qnnj text__373c0__2Kxyz comment__373c0__3EKjH text-color--normal__373c0__3xep9 text-align--left__373c0__2XGa-'}):
    #         per_review = i.find('span')
    #         # print(per_review)
    #         review.append(per_review)
    #
    #     new_review = []
    #     for each in review:
    #         new_each = str(each).replace('<br/>', '')
    #         new_each = str(new_each).replace('&amp;', '')
    #         new_each = str(new_each).replace(':p', '')
    #         new_each = str(new_each).replace(':P', '')
    #         new_each = str(new_each).replace(':)', '')
    #         new_each = new_each[68:-7]
    #         print(new_each)
    #         new_review.append(new_each)
    #
    #     return new_review
    #





#        for i in range(len(review_list)):
#            r = requests.post(
#                "https://api.deepai.org/api/sentiment-analysis",
#                data={
#                    'text': review_list[i],
#                },
#                headers={'api-key': 'YOUR-API-KEY'}
#            )
#            i = i + 1
#
#            data = r.json()
#            self.lbl.text = str(data['output'])


class Sentimento(App):

    def build(self):
        self.screen_manager = ScreenManager()

        self.main_page = MainPage()
        screen = Screen(name="Main")
        screen.add_widget(self.main_page)
        self.screen_manager.add_widget(screen)

        self.search_page = SearchPage()
        screen = Screen(name="Search")
        screen.add_widget(self.search_page)
        self.screen_manager.add_widget(screen)

        self.result_page = ResultPage()
        screen = Screen(name="Result")
        screen.add_widget(self.result_page)
        self.screen_manager.add_widget(screen)

        self.app_page = AppPage()
        screen = Screen(name="App")
        screen.add_widget(self.app_page)
        self.screen_manager.add_widget(screen)

        return self.screen_manager

if __name__ == "__main__":
    sentimento = Sentimento()
    sentimento.run()
