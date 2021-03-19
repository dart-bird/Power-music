import requests
import json
from bs4 import BeautifulSoup
from youtube_search import YoutubeSearch

def get_html(url):
    html = requests.get(url, headers={"User-Agent": "XY"})
    soup = BeautifulSoup(html.text, 'html.parser')
    return soup

def get_songs_top_rank100(song_code):
    soup = get_html('https://www.melon.com/chart/month/index.htm?classCd=' + song_code)
    song_title_elements = soup.find_all("div", class_="ellipsis rank01")
    song_singer_elements = soup.find_all("div", class_="ellipsis rank02")
    song_album_elements = soup.find_all("div", class_="ellipsis rank03")
    
    songs = []
    
    for idx in range(len(song_title_elements)-1):
        song_data = {
            "title" : song_title_elements[idx].find_all("a")[0].text,
            "singer" : song_singer_elements[idx].find_all("a")[0].text,
            "album" : song_album_elements[idx].find_all("a")[0].text
        }
        songs.append(song_data)

    return songs

def get_yt_link(title):
    results = json.loads(YoutubeSearch(title, max_results=1).to_json())
    return 'https://www.youtube.com' + results['videos'][0]['url_suffix']

if __name__ == "__main__":
    songs = get_songs_top_rank100('GN0100') #GN0100 발라드
    print(get_yt_link(songs[0]['title']))
