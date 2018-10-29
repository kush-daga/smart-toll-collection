import requests
import bs4
res = requests.get('http://tweeplers.com/hashtags/?cc=IN')
soup = bs4.BeautifulSoup(res.text,'lxml')
new = soup.find_all( class_='wordwrap')
titles=[]
for ans in new:
    titles.append(ans.text)

print(titles)