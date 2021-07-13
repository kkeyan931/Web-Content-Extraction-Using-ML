import page_clustering



clt = page_clustering.OnlineKMeans(n_clusters=5)

pages = ["https://ziyan.net/2014/04/web-content-extraction-through-machine-learning","https://pypi.org/project/pyttsx3/"]
for page in pages:
    clt.add_page(page)

y = clt.classify()