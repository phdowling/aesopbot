import json
import requests
from bs4 import BeautifulSoup
import codecs

with open("token.txt", "r") as inf:
    token = inf.readline().strip()

base_url = "http://api.genius.com%s?access_token=" + token
artists_url = "http://api.genius.com/artists/%s/songs?per_page=50&page=%s&access_token=" + token


def handle_song_url(url):
    lyrics_html = requests.get(url).text
    soup = BeautifulSoup(lyrics_html, "lxml")
    lyrics = soup.findAll('div', {"class": "song_body-lyrics"})[0].text
    return lyrics


def iterate_artist_songs(artist_id):
    page = 1
    page_one = artists_url % (artist_id, page)
    res = json.loads(requests.get(page_one).content)
    for song in res["response"]["songs"]:
        yield handle_song_url(song["url"])

    while res["response"]["next_page"]:
        page += 1
        print "On page %s" % page
        next_page = artists_url % (artist_id, page + 1)
        res = json.loads(requests.get(next_page).content)
        for song in res["response"]["songs"]:
            yield handle_song_url(song["url"])

ARTISTS = {
    "Kanye West": 72,
    "Kendrick Lamar": 1421,
    "Jay Z": 2,
    "Mos Def": 156
}

if __name__ == "__main__":
    ARTIST = "Kanye West"
    with codecs.open("all_lyrics_kanye.txt", "w", "utf-8") as outf:
        for idx, lyrics in enumerate(iterate_artist_songs(ARTISTS[ARTIST])):
            if idx % 500 == 0:
                print "got %s lyrics.." % idx
            outf.write(lyrics + u"\n\n\n")
