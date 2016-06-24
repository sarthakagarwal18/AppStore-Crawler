from bs4 import BeautifulSoup
import requests
import time

class AppCrawler:

	def __init__(self, starting_url, depth):
		self.starting_url = starting_url
		self.depth = depth
		self.current_depth = 0
		# links found at a certain depth
		self.depth_links = []
		self.apps = []

	def crawl(self):
		app = self.get_app_from_link(self.starting_url)
		self.apps.append(app)
		self.depth_links.append(app.links)

		while self.current_depth < self.depth:
			current_links = []
			for link in self.depth_links[self.current_depth]:
				current_app = self.get_app_from_link(link)
				current_links.extend(current_app.links)
				self.apps.append(current_app)
				# if we make many requests at the same time, we might get blacklisted.
				# hence requests are made every 2 sec. Drawback:Makes the Crawler Slow.
				# Comment it out for use.
				# time.sleep(2)
			self.current_depth += 1
			self.depth_links.append(current_links)


	def get_app_from_link(self, link):
		response = requests.get(link)
		source_code = response.text
		soup = BeautifulSoup(source_code, "html.parser")
		name = soup.find('h1', {'itemprop': 'name'}).string
		dev = soup.find_all('div', {'class': 'intro'})
		for tag in dev:
			developer = tag.find('h2').string;
		price = soup.find('div', {'itemprop': 'price'}).string
		link_name = soup.find_all('div', {'class': 'center-stack'})
		for link in link_name:
			app_link = link.find_all('a', {'class': 'name'})
		links = []
		for linked in app_link:
			links.append(linked.get('href'))

		app = App(name, developer, price, links)

		return app



class App:

	def __init__(self, name, developer, price, links):
		self.name = name
		self.developer = developer
		self.price = price
		self.links = links

	def __str__(self):
		return ("Name: " + str(self.name.encode('utf-8'))[2:-1] +
		"\r\nDeveloper: " + self.developer + 
		"\r\nPrice: " + self.price + "\r\n")


crawler = AppCrawler('https://itunes.apple.com/us/app/candy-crush-saga/id553834731', 2)
crawler.crawl()

for app in crawler.apps:
	print (app)
