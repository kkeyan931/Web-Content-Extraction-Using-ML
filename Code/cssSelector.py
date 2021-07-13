from bs4 import BeautifulSoup as BSoup
import cssutils
import requests

import pandas as pd

import logging

cssutils.log.setLevel(logging.CRITICAL)

selectors = {}

URL = "https://www.ndtv.com/india-news/ndtv-news-on-oxygen-supply-cited-by-delhi-high-court-2418022"
page = requests.get(URL)

soup = BSoup(page.content, 'html5lib')

attrs = []
tags = []

for tag in soup.findAll(True):
    tags.append(tag.name)
    attrs.append(tag.attrs)

tagsClass = []

for attr in attrs:
    tagsClass.append(attr.get("class"))

classList = []
for i in tagsClass:
    if i:
        for j in i:
            classList.append(j)

uniqueClass = list(set(classList))

data = []
zeroes = [0 for i in range(len(uniqueClass))]

for iClass in tagsClass:
    row=[]
    if iClass:
        for j in uniqueClass:
            if j in iClass:
                row.append(1)
            else:
                row.append(0)
        data.append(row)
    else:
        data.append(zeroes)


df = pd.DataFrame(columns=uniqueClass,data=data)

print(df.head())




# for i in attrs:
#     print(i)
#
#
# for styles in soup.select('style'):
#     css = cssutils.parseString(styles.encode_contents())
#     for rule in css:
#         if rule.type == rule.STYLE_RULE:
#             style = rule.selectorText
#             selectors[style] = {}
#             for item in rule.style:
#                 propertyname = item.name
#                 value = item.value
#                 selectors[style][propertyname] = value
#
# for i,j in selectors.items():
#     print(i)
#     print(j)
#     print("---------------------------------------------------------------------------------------\n")
