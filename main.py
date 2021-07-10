import requests._internal_utils
from bs4 import BeautifulSoup
import datetime
import uyts

class Melon_to_yt:
    def __init__(self):
        self.code = [
            'GN0000','DM0000','AB0000',
            'GN0100','GN0200','GN0300','GN0400','GN0500','GN0600','GN0700','GN0800',
            'GN0900','GN1000','GN1100','GN1200','GN1300','GN1400',
            'GN1500','GN1700','GN1800','GN1900','GN2000','GN2100','GN2200','GN2300','GN2400',
        ]
    
    def __get_response(self, url):
        return requests.get(url, headers={
            'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
        })

    def __get_songs_melon_chart_100(self, time, song_code):
        url='https://www.melon.com/chart/{0}/index.htm?classCd={1}'.format(time, song_code)
        if time not in ['day','week','month']:
            now = datetime.datetime.now()
            day_time = str(now.year) + "{:02d}".format(now.month) + "{:02d}".format(now.day) + "{:02d}".format(now.hour) + '00'
            url='https://www.melon.com/chart/index.htm?dayTime='
        response = self.__get_response(url)
        soup = BeautifulSoup(response.text, 'html.parser')
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
        self.songs = songs
        return songs
    def __search_yt(self, title : str):
        masking_word = ['1hour', '1시간', '연속재생', '플레이리스트', 'playlist', '풀영상']
        search = uyts.Search(title)
        # skip video data format like 1hour, playlist ... etc
        for video in search.resultsJSON:
            filtered = list(filter(lambda x:x in video['title'], masking_word))
            if len(filtered) < 1:
                return video
            else : continue
    def get_yt_data(self, time : str, code = 'GN0100') -> list:
        if code in self.code:
            self.__get_songs_melon_chart_100(time=time, song_code=code)
            yt_data = []
            for song in self.songs:
                yt_data.append(self.__search_yt(song['title']))
                print('{0} of {1} Searched Music! Title : {2}'.format(
                    len(self.songs),
                    len(yt_data),
                    yt_data[len(yt_data)-1]['title']))
            return yt_data
        else:
            return []

if __name__ == "__main__":
    melon = Melon_to_yt()
    now = datetime.datetime.now()
    day_time = str(now.year) + "{:02d}".format(now.month) + "{:02d}".format(now.day) + "{:02d}".format(now.hour) + '00'
    video1 = melon.get_yt_data(time=day_time,code='GN0100')
    video2 = melon.get_yt_data(time='day',code='GN0100')
    video3 = melon.get_yt_data(time='month',code='GN0100')
    video4 = melon.get_yt_data(time='year',code='GN0100')
    print(video1, video2, video3, video4)
