#!/usr/bin/env python
# coding: utf-8

# In[102]:


import requests
import pandas as pd
import pymongo
from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from flask import Flask, render_template, redirect


# In[11]:
#  Create flask app
app = Flask(__name__)

# Connect to MongoDB
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

# Use database and create it
db = client.marsDB
collection = db.marsdata

mars_news_url = 'https://redplanetscience.com'
mars_news_html = requests.get(mars_news_url)


# In[18]:


#Parse the website w/ BeautifulSoup
mars_soup = BeautifulSoup(mars_news_html.text, 'html.parser')



# In[19]:


print(mars_soup.prettify)


# In[14]:


news_title = 'NASA Invites Students to Name Mars 2020 Rover'
news_paragraph = "Through Nov. 1, K-12 students in the U.S. are encouraged to enter an essay contest to name NASA's next Mars rover."


# In[15]:


article_titles = mars_soup.find_all('div', class_='content_title')
article_titles


# In[20]:


for article in article_titles:
    title = article.find('a')
    title_text = title.text
    print(title_text)


# In[33]:


executable_path = {'executable_path': ChromeDriverManager().install()}
mars_images_browser = Browser('chrome', **executable_path, headless=False)


# In[34]:


nasa_url = 'https://spaceimages-mars.com/'
mars_images_browser.visit(nasa_url)


# In[35]:


# Parse html file with BeautifulSoup
mars_images_html = mars_images_browser.html
nasa_soup = BeautifulSoup(mars_images_html, 'html.parser')


# In[36]:


images = nasa_soup.find_all('div', class_='carousel_items')
images


# In[43]:


featured_image_url = f'https://spaceimages-mars.com/image/featured/mars1.jpg'


# In[44]:


print(featured_image_url)


# In[45]:


MarsFactsURL = "https://galaxyfacts-mars.com"


# In[71]:


mars_df = pd.read_html(MarsFactsURL)
mars_df


# In[76]:


mars1_df = mars_df[1]
mars1_df


# In[78]:


mars2_df = mars1_df.transpose()
mars2_df


# In[80]:


mars2_df.columns = [
    'Equatorial diameter',
    'Polar diameter',
    'Mass',
    'Moons',
    'Orbit distance',
    'Orbit period',
    'Surface temperature',
    'First record',
    'Recorded by'
]
mars2_df


# In[81]:


clean_mars_facts_df = mars2_df.iloc[1:]


# In[82]:


clean_mars_facts_df


# In[124]:


mars_facts_html_table = clean_mars_facts_df.to_html()
print(mars_facts_html_table)


# In[125]:


usgs_browser = Browser('chrome', **executable_path, headless=False)
usgs_url = "https://marshemispheres.com/"
usgs_browser.visit(usgs_url)


# In[127]:


mars_hemispheres_html = usgs_browser.html
mars_hemispheres_soup = BeautifulSoup(mars_hemispheres_html, 'html.parser')


# In[128]:


print(mars_hemispheres_soup.body.prettify())


# In[129]:


mars_hemispheres = mars_hemispheres_soup.find_all('div', class_='description')
mars_hemispheres


# In[133]:


# Create list of dictionaries to hold all hemisphere titles and image urls
hemisphere_image_urls = []

# Loop through each link of hemispheres on page
for image in mars_hemispheres:
    hemisphere_url = image.find('a', class_='itemLink')
    hemisphere = hemisphere_url.get('href')
    hemisphere_link = 'https://astrogeology.usgs.gov/' + hemisphere
    print(hemisphere_link)

    # Visit each link that you just found (hemisphere_link)
    usgs_browser.visit(hemisphere_link)
    
    # Create dictionary to hold title and image url
    hemisphere_image_dict = {}
    
    # Need to parse html again
    mars_hemispheres_html = usgs_browser.html
    mars_hemispheres_soup = BeautifulSoup(mars_hemispheres_html, 'html.parser')
    
    # Get image link
    hemisphere_link = mars_hemispheres_soup.find("img", class_="browse")["src"]
    
    # Get title text
    hemisphere_title = mars_hemispheres_soup.find('a').string
    
    # Append title and image urls of hemisphere to dictionary
    hemisphere_image_dict['title'] = hemisphere_title
    hemisphere_image_dict['img_url'] = hemisphere_link
    
    # Append dictionaries to list
    hemisphere_image_urls.append(hemisphere_image_dict)

print(hemisphere_image_urls)


# In[134]:


get_ipython().system(' jupyter nbconvert --to script --template basic mission_to_mars.ipynb --output scrape_mars')


# In[ ]:




