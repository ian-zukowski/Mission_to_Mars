# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager

import pandas as pd
import numpy as np


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


df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['Description', 'Mars', 'Earth']
df.set_index('Description', inplace=True)
df


df.to_html()


# ### HEMISPHERES

# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'

browser.visit(url)


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
html = browser.html
hemisphere_soup = soup(html, 'html.parser')
hemi_urls = hemisphere_soup.find_all('img', class_='thumb')

for item in hemi_urls:
    hemi_rel_url = item.get('src')
    hemi_img_url = f'https://marshemispheres.com/{hemi_rel_url}'
    hemisphere_image_urls.append(hemi_img_url)

hemisphere_image_urls


# 2. Create a list to hold the images and titles.
hemisphere_urls_layer1 = []
hemisphere_image_urls = []
hemispheres = {}

# 3. Write code to retrieve the image urls and titles for each hemisphere.
html = browser.html
hemisphere_soup = soup(html, 'html.parser')
hemi_urls = hemisphere_soup.find_all('a', class_='itemLink product-item')

for item in hemi_urls:
    hemi_rel_url = item.get('href')
    hemi_img_url = f'https://marshemispheres.com/{hemi_rel_url}'
    if hemi_img_url not in hemisphere_urls_layer1:
        hemisphere_urls_layer1.append(hemi_img_url)

for link in hemisphere_urls_layer1:
    url = link
    browser.visit(url)
    html = browser.html
    hemisphere_soup_layer2 = soup(html, 'html.parser')
    try:
        hemi2_title = hemisphere_soup_layer2.find('h2', class_='title').get_text()
        hemi2_urls = hemisphere_soup_layer2.find('li')
        hemi2_box = hemi2_urls.find_all('a')
        for item in hemi2_box:
            hemi2_rel_url = item.get('href')
            hemi2_full_url = f'https://marshemispheres.com/{hemi2_rel_url}'
            hemispheres["img_url"]=hemi2_full_url
            hemispheres["title"]=hemi2_title
        print(hemispheres)
        hemisphere_image_urls.append(hemispheres)
    except:
        pass


hemisphere_image_urls

