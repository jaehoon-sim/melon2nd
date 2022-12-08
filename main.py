from flask import Flask, render_template
from django.shortcuts import render
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)


def crawler_melon():
  header = {
    'User-Agent':
    'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'
  }
  req = requests.get('https://www.melon.com/chart/week/index.htm',
                     headers=header)
  html = req.text
  parse = BeautifulSoup(html, 'html.parser')

  titles = parse.find_all("div", "ellipsis rank01")
  singer = parse.find_all("span", "checkEllipsis")
  song_detail = parse.find_all("a", "song_info")
  album_detail = parse.find_all("a", "image_typeAll")

  song = []
  songs_detail = []
  artist = []
  artist_detail = []
  thumbnail = []
  albums_detail = []

  for u in parse.select("span.checkEllipsis"):
    u = u.find('a')
    u = u.get('href')
    artist_detail.append(u)

  for sd in song_detail:
    sd = sd.get('href')
    songs_detail.append(sd)

  for ad in album_detail:
    ad = ad.get('href')
    albums_detail.append(ad)

  for t in titles:
    song.append(t.text.replace("\n", ""))

  for s in singer:
    artist.append(s.text.replace("\n", ""))

  for thumbs_img in parse.select(".image_typeAll"):
    thumbs_img = thumbs_img.find("img")
    thumbs_img = thumbs_img.get("src")
    thumbnail.append(thumbs_img)

  return [song, artist, thumbnail, artist_detail, songs_detail, albums_detail]


result = crawler_melon()


@app.route('/')
def index():
  song = result[0]
  artist = result[1]
  thumbnail = result[2]
  artist_detail = result[3]
  songs_detail = result[4]
  albums_detail = result[5]
  count = len(song)
  return render_template('index.html',
                         song=song,
                         artist=artist,
                         count=count,
                         thumbnail=thumbnail,
                         artist_detail=artist_detail,
                         songs_detail=songs_detail,
                         albums_detail=albums_detail)
  # return render('index.html',
  #               song=song,
  #               artist=artist,
  #               count=count,
  #               thumbnail=thumbnail,
  #               artist_detail=artist_detail,
  #               songs_detail=songs_detail,
  #               albums_detail=albums_detail)


if __name__ == '__main__':
  app.run(debug=False)