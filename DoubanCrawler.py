import expanddouban
import urllib
import bs4
import time
import csv
import codecs

category = ['剧情','科幻','动作']
location = ['大陆','美国','香港','台湾','日本','韩国','英国','法国','德国','意大利','西班牙','印度','泰国','俄罗斯','伊朗','加拿大','澳大利亚','爱尔兰','瑞典','巴西','丹麦']

def getMovieUrl(category,location):
	 return "https://movie.douban.com/tag/#/?sort=S&range=9,10&tags=电影,{},{}".format(category,location)

class Movie:
    def __init__(self, name,rate,location,category,info_link,cover_link):
        self.name = name
        self.rate = rate
        self.location = location
        self.category = category
        self.info_link = info_link
        self.cover_link = cover_link
    def print_data(self):
        return self.name, self.rate, self.location, self.category, self.info_link, self.cover_link
def getMovies(category, location):
	movies = []
	html = expanddouban.getHtml(getMovieUrl(category, location),True)
	soup = bs4.BeautifulSoup(html,"html.parser")
	content_div = soup.find(id='content').find(class_='list-wp').find_all('a',recursive=False)
	for element in content_div:
		M_name = element.find(class_='title').string
		M_rate = element.find(class_='rate').string
		M_category = category
		M_location = location
		M_info_link = element.get('href')
		M_cover_link = element.find('img').get('src')
		movies.append(Movie(M_name,M_rate,M_category,M_location,M_info_link,M_cover_link).print_data())
	return movies		


rate_9= []
movie_category_number = {}
movie_category_location_number = {}
for i in category:
	number1 = 0
	for j in location:
		number2 = 0
		for k in getMovies(i, j):
			rate_9.append(k)
			number1 += 1
			number2 += 1
		movie_category_number[i] = number1
		movie_category_location_number[i,j] = number2
rank_movie_category_location_number = sorted(movie_category_location_number.items(),key=lambda d: d[1],reverse = True)

story_three = []
story_percent = []
for i in rank_movie_category_location_number:
	category_name = i[0][0]
	if category_name == category[0]:
		ratio = i[1] / movie_category_number[category[0]]
		story_percent.append(ratio)
		story_three.append(i[0][1])
	if len(story_three) == 3:
		break
		
science_three = []
science_percent = []
for i in rank_movie_category_location_number:
	category_name = i[0][0]
	if category_name == category[1]:
		ratio = i[1] / movie_category_number[category[1]]
		science_percent.append(ratio)
		science_three.append(i[0][1])
	if len(science_three) == 3:
		break

action_three = []
action_percent = []
for i in rank_movie_category_location_number:
	category_name = i[0][0]
	if category_name == category[2]:
		ratio = i[1] / movie_category_number[category[2]]
		action_percent.append(ratio)
		action_three.append(i[0][1])
	if len(action_three) == 3:
		break
		
with codecs.open('movies.csv','w','utf_8_sig') as f:
	writer = csv.writer(f)
	writer.writerows(rate_9)
with open('output.txt','w',encoding='utf-8') as f:
	f.write("{}电影前三地区排名：{},{},{}，百分比为：{:.2%},{:.2%},{:.2%}\n".format(category[0],story_three[0],story_three[1], story_three[2], story_percent[0],story_percent[1], story_percent[2]))
	f.write("{}电影前三地区排名：{},{},{}, 百分比为：{:.2%},{:.2%},{:.2%}\n".format(category[1],science_three[0],science_three[1], science_three[2], science_percent[0],science_percent[1], science_percent[2]))
	f.write("{}电影前三地区排名：{},{},{}，百分比为：{:.2%},{:.2%},{:.2%}".format(category[2],action_three[0],action_three[1], action_three[2], action_percent[0],action_percent[1], action_percent[2]))
