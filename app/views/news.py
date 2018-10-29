import requests
import bs4
import string
res = requests.get('https://www.google.com/search?q=%23metoo&source=lnms&tbm=nws&sa=X&ved=0ahUKEwizy_nQx6feAhVKFHIKHYUpAyQQ_AUIDygC&biw=1366&bih=641')
soup = bs4.BeautifulSoup(res.text, 'lxml')
print(soup)
new = soup.find_all(class_="r")
print(new)
titles=[]

for ans in new:
	print(ans)
	url =ans.a.get('href')
	url = url.replace('/url?q=','')
	p = url.find('&sa=U')
	titles.append(url[:p])
print(titles)