from facebook_scraper import get_posts

for post in get_posts('Netrobe-Developments-103024651259550'):
	print(post['text'])