# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager

import pandas as pd
import datetime as dt

executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)

html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')

news_title = slide_elem.find('div', class_='content_title').get_text()

print(news_title)

# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### FEATURED IMAGES
# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)

# Find and click the full image button
# Need to use index 1, because index 0 is a button that brings up nav menu, then index 1 is the featured image we want
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()

# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')

# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel

# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# ### MARS FACTS TABLE

df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['Description', 'Mars', 'Earth']
df.set_index('Description', inplace=True)
df

df.to_html()


# ### HEMISPHERES

# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'

browser.visit(url)

hemisphere_image_urls = []

html = browser.html
hemisphere_soup = soup(html, 'html.parser')
hemi_urls = browser.find_by_css('a.product-item img')

for i in range(len(hemi_urls)):
    hemispheres = {}
    browser.find_by_css('a.product-item img')[i].click()
    sample_elem = browser.links.find_by_text('Sample').first
    hemispheres['img_url'] = sample_elem['href']
    hemispheres['title']= browser.find_by_css('h2.title').text
    hemisphere_image_urls.append(hemispheres)
    
    browser.back()

browser.quit()

