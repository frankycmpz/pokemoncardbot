import requests
from bs4 import BeautifulSoup
from urllib.error import HTTPError
from urllib.request import urlretrieve
import tweepy
import re


headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    }

#pokemon twitter account keys go

consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

def final():
    url = "https://www.pkmncards.com/?random"
    req = requests.get(url, headers)
    soup = BeautifulSoup(req.content, 'html.parser')


    cardimage = soup.find("a", class_= "card-image-link")

    #image link
    link = cardimage.get("href")
    print(link +" -- link to be downloaded")
    filepath = downloadImage(link)


    text = soup.find("div", class_="name-hp-color")

    #name
    name_class = text.find("span",class_="name")
    name = name_class.get_text()

    text = soup.find("div", class_="release-meta minor-text")

    #set
    setdata = text.find("span", title="Set")
    setname = setdata.get_text()

    #number
    num_unformat = text.find("span", class_ = "number-out-of")
    num = num_unformat.find("span", class_="number").get_text()
    setnum = num_unformat.find("span", class_="out-of").get_text()

    #price
    price = soup.find("div", class_="list").find("li", class_="m").get_text().lstrip()
    print(price)
    price = re.sub("[^0-9]", "", price)
    price = "$"+price[:-2] +"."+price[-2:]

    #what will be tweeted
    draft = name +'\n\n'+num+setnum +' — '+setname+"\nMarket price: "+price

    print("\n\n FINAL OUTPUT:\n\n" +draft)
    content = [filepath, draft]

    tweet(content)


def tweet(content):
    media_ids = []

    res = api.media_upload(content[0])
    media_ids.append(res.media_id)
    text = content[1]

    api.update_status(text, media_ids=media_ids)


def downloadImage(url):
    print(url +" -- downloading image")

    filepath = "/home/franky/developer/pokebot/test.jpg"
    print(filepath +" -- filepath image located at")

    try:
        urlretrieve(url, filepath)
        print("success -- image downloaded")
        return filepath

    except FileNotFoundError as err:
        print("path error")   # something wrong with local path
    except HTTPError as err:
        print("url error")  # something wrong with url


if __name__ == '__main__':
    final()