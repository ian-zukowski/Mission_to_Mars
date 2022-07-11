# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager

import pandas as pd
import datetime as dt

def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in dictionary
    data = {
      "news_title": news_title,
      "news_paragraph": news_paragraph,
      "featured_image": featured_image(browser),
      "facts": mars_facts(),
      "url": hemispheres,
      "last_modified": dt.datetime.now()
    }

    # Quit the browser
    browser.quit()
    return data

### NASA NEWS SITE

def mars_news(browser):

    # Visit the mars nasa news site
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    # Account for attribute errors 
    except AttributeError:
        return None, None

    # Return the functioning news_title and paragraph
    return news_title, news_p



# ### JPL SPACE IMAGES FEATURED IMAGES

def featured_image(browser):

    # Visit URL for featured image
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    # Need to use index 1, because index 0 (the first button in the code) is a button that brings up nav menu. Index 1 is the featured image we want.
    full_image_button = browser.find_by_tag('button')[1]
    full_image_button.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Find the relative image url
    # the "fancybox-image" class is only present for the full-screen version of the featured image
    try:
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    # Combine the base URL and relative image url to create a fully functional URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    # Return the functional URL
    return img_url


# ## Mars Facts

def mars_facts():

    # Use lxml and pandas to read in the html code from the galaxyfacts website and create a dataframe from the table
    # The [0] allows it to call on the first table in the code -- which happens to be a Mars/Earth comparison table
    # Would want to change index to [1] and columns to only [description,Mars] if we want the table at the top right of the page
    try:
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
        df.columns=['Description', 'Mars', 'Earth']
        df.set_index('Description', inplace=True)

    except BaseException:
        return None

    # Read the df back to html to make it compatible with future web app
    return df.to_html(classes='table table-striped')

def hemispheres(browser):
    # 1. Use browser to visit the URL 
    url = 'https://marshemispheres.com/'

    browser.visit(url)

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

if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())