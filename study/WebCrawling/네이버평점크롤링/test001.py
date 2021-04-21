import requests
from bs4 import BeautifulSoup
#select는 만족하는 여러 인스턴스를 찾고, find는 첫 번째 인스턴스를 반환합니다.
def get_movie_point(start, end):
    result = []
    for i in range(start, end+1):
        url = 'https://movie.naver.com/movie/point/af/list.nhn?&page={}'.format(i)
        r = requests.get(url)
        bs = BeautifulSoup(r.text, "lxml")

        trs = bs.select("table.list_netizen > tbody > tr")
        for tr in trs:#다수의 평점
            # td = tr.select("td")
            # title= td[1].select("a")[0].text
            # score=tr.find("div",{"class":"list_netizen_score"}).find("em").text
            # print(title, score)

            content=tr.find("td",{"class","title"}).text
            content=content.split('\n')
            content="\n".join(content[0:6])
            print(content)
            print()
get_movie_point(1,2)