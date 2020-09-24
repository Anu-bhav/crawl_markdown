#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests, re, os
from bs4 import BeautifulSoup
from pprint import pprint
from collections import OrderedDict

url = "https://networklessons.com/cisco/ccna-200-301"
req = requests.get(url)
soup = BeautifulSoup(req.text, "html.parser")
print(soup.title.text.split('|')[0])

spans = soup.find_all("ul", {"class":"bellows-nav"})


# In[2]:


title_list = []
links_list = OrderedDict()

for span in spans:
    for title in span.find_all("span", {"class":"bellows-target-title"}):
        text = title.text.replace(":", " -")
        title_list.append(text)

    for item2 in span.find_all("a", {"class":"bellows-target"},href=True):
        links_list[item2.text] = item2['href']

# pprint(title_list)
# pprint(links_list)


# In[3]:


unit_index = []

for i, item in enumerate(title_list):
    if "Unit " in item:
        unit_index.append(i)

for i in unit_index:
    pass
    # print(i, title_list[i])

links_index = []
links_index_to_links_list = []
for link in links_list:
    # print(link)
    links_index.append([index for index, num in enumerate(title_list) if link in num][0])
    

# print(links_index)

# print(len(title_list))
# print(len(links_list))


# In[4]:


# count = 1
for i, unit in enumerate(unit_index):
    for link in links_index:
        try:
            # print(link, unit, unit_index[i + 1])
            if (unit < link) and (link < unit_index[i + 1]):
                print(title_list[unit], " ---- ", title_list[link], " ---- ", links_list[title_list[link]])
                # print(count)
                # count+=1
        except (IndexError, ValueError):
            break


# In[5]:


def make_dir(path):
    download_path = os.path.join(os.getcwd(), "Markdown Output\\", path)
    os.makedirs(download_path, exist_ok=True)


# In[6]:


# Make Output Directories

course = soup.title.text.split('|')[0].strip()

for i in unit_index:
    path = course + "\\" + title_list[i]
    # print(path)
    make_dir(path)
    download_path = os.path.join(os.getcwd(), "Markdown Output\\", path)
    print(download_path)


# In[35]:


import pyautogui, os, requests, re
from msedge.selenium_tools import Edge, EdgeOptions, webdriver

options = EdgeOptions()
options.use_chromium = True
unpacked_extension_path = os.path.join(os.getcwd(), "markdown-clipper")
options.add_argument("--load-extension={}".format(unpacked_extension_path))
download_path = os.path.join(os.getcwd(), "Markdown Output\\")
prefs = {"download.default_directory": download_path, "profile.default_content_settings.popups": 0, "directory_upgrade": True}
options.add_experimental_option("prefs", prefs)
options.add_experimental_option("detach", True)
driver = Edge(options=options)

url = "https://networklessons.com/cisco/ccna-200-301"
driver.get(url)


# In[43]:


agree = driver.find_elements_by_xpath('//*[@id="catapult-cookie-bar"]/div/div')
join = driver.find_elements_by_xpath('//*[@id="om-mvhsujbebu4nqhlzcsgs-optin"]/div/button')

if agree:
    agree[0].click()

if join:
    join[0].click()


# In[ ]:




