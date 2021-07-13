import requests
from bs4 import BeautifulSoup
import pandas as pd
import heapq

import Lcs

from itertools import compress

import pylcs as LCS

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN

from sklearn.model_selection import train_test_split
from sklearn.svm import SVC

from sklearn.metrics import f1_score,confusion_matrix

# Html Extraction
# URL = 'https://www.geeksforgeeks.org/implementing-web-scraping-python-beautiful-soup/'
URL = "https://www.ndtv.com/india-news/ndtv-news-on-oxygen-supply-cited-by-delhi-high-court-2418022"
page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html5lib')

# Extracting Meta Content
meta = []
for tag in soup.findAll(True):
    if tag.name == "meta":
        meta.append(tag.attrs)

metaContent = []
for dic in meta:
    metaContent.append(dic["content"])

noise = ["https", ".com", "com.", "www", "@", ":", "=", "#"]
metaContentFinal = []
for content in metaContent:
    if any(i in content for i in noise):
        pass
    else:
        metaContentFinal.append(content)

metaContentStr = ""

for content in metaContentFinal:
    metaContentStr = metaContentStr + content

# tags, texts, attribute Extraction

tags = []
texts = []
attrs = []

for tag in soup.findAll(True):
    if (tag.name == "style") or (tag.name == "script") or (tag.name == "body") or (tag.name == "div") or (tag.name == "html") or (tag.name == "head"):
        continue
    else:
        tags.append(tag.name)
        texts.append(tag.text)
        attrs.append(tag.attrs)

texts = pd.Series(texts)
column = list(set(tags))

data = []

for i in range(0, len(tags)):
    data1 = []
    for j in range(0, len(column)):
        if tags[i] == column[j]:
            data1.append(1)
        else:
            data1.append(0)
    data.append(data1)

df = pd.DataFrame(columns=column, data=data)

textSize = []

for text in texts:
    textSize.append(len(text))

df["textSize"] = textSize

attrsColumn = []
for i in attrs:
    attrsColumn.append(list(i.keys()))

attrsColumn = sum(attrsColumn, [])

attrsColumn = list(set(attrsColumn))

data = []
for i in attrs:
    idx = []
    for j in i.keys():
        for k in range(0, len(attrsColumn)):
            if j == attrsColumn[k]:
                idx.append(k)

    data.append([1 if i in idx else 0 for i in range(0, len(attrsColumn))])

df1 = pd.DataFrame(columns=attrsColumn, data=data)

finalDf = pd.concat([df, df1], axis=1, join='inner')

keywords = ["await", "break", "case", "catch", "class", "const", "continue", "debugger",
            "default", "delete", "do", "else", "enum", "export", "extends", "false",
            "finally", "for", "function", "if", "implements", "import", "in", "instanceof", "interface",
            "let", "new", "null", "package", "private", "protected", "public", "return", "super", "switch",
            "static", "throw", "try", "true", "typeof", "var", "void", "while", "with", "yield",
            "(", ")", "{", "}", "]", "[", ";", ".", "\"", "function", "console", "cmd", "display", "push",
            "window", "href", "\'", "return"]


data=[]
for i in str(texts):
    data1=[]
    for j in keywords:
        c = i.count(j)
        data1.append(c)
    data.append(data1)


df1 = pd.DataFrame(columns=keywords, data=data)
finalDf = pd.concat([finalDf, df1], axis=1, join='inner')



#CSS Class features

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

finalDf = pd.concat([finalDf, df], axis=1, join='inner')


# Normalization

std = StandardScaler()

finalDf = std.fit_transform(finalDf)

finalDf = pd.DataFrame(finalDf)

# DBSCAN Clustering

clustering = DBSCAN().fit(finalDf)

uniqueClusters = set(clustering.labels_)

finalDf["cluster"] =[i+1 for i in clustering.labels_]

print(finalDf.head())

# c = -1
#
# idx = []
# for i in clustering.labels_:
#     if i == c:
#         idx.append(1)
#     else:
#         idx.append(0)

# print(list(compress(tags, idx)))


score = [0 for i in range(len(uniqueClusters))]

# print(finalDf.shape)

for i in range(0, finalDf.shape[0]):
    score[int(finalDf.loc[i]["cluster"])] = score[int(finalDf.loc[i]["cluster"])] + LCS.lcs(metaContentStr,
                                                                                                  texts[i])



print("Score of Each Cluster")
print(score)

print()
print("Clusters with high Score")

maxScoreClusters = heapq.nlargest(2, range(len(score)), key=score.__getitem__)
print(maxScoreClusters)

label = []

for i in range(0,finalDf.shape[0]):
    if (int(finalDf.loc[i]["cluster"]) == maxScoreClusters[0]) or (int(finalDf.loc[i]["cluster"]) == maxScoreClusters[1]):
        label.append(1)
    else:
        label.append(0)

# for i in range(0, finalDf.shape[0]):
#     if int(finalDf.loc[i]["cluster"]) == 16:
#         print(tags[i])
#         print()
#         print(texts[i])
#         print(
#             "--------------------------------------------------------------------------------------------------------\n")


# SVM Classification

finalDf["label"] = label

print(finalDf.head())

finalDf = finalDf.drop(columns="cluster")

X = finalDf.drop(columns="label")
y = finalDf["label"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)


svmModel = SVC()
svmModel.fit(X_train,y_train)

prediction = svmModel.predict(X_test)

print("F1 Score of SVM Model")
f1Score = f1_score(y_test,prediction)
print(f1Score)

print()

print("Confusion Matrix")

print(confusion_matrix(y_test,prediction))
