import requests
def getTopStories():
    return requests.get('https://newsapi.org/v2/top-headlines?country=us&apiKey=45e32894443047b8bde86b7d9ce8720d')