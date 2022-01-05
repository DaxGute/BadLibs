import newsAPI
import json
import spacy

nlp = spacy.load("en_core_web_sm")

class WebScraping:
    def __init__(self):
        self.r = newsAPI.getTopStories().json()

    def getTitlesAndDesriptions(self):
        articleTitles = []
        articleDesc = []
        for article in self.r['articles']:
            articleTitles.append(article['title'])
            articleDesc.append(article['description'])
        return articleTitles, articleDesc

    def getTitles(self):
        articleTitles = []
        for article in self.r['articles']:
            articleTitles.append(article['title'])
        return articleTitles

    def getDescriptions(self):
        articleDesc = []
        for article in self.r['articles']:
            articleDesc.append(article['description'])
        return articleDesc

if __name__ == "__main__":
    newInstance = WebScraping()
    titles, desc = newInstance.getTitlesAndDesriptions()
    text = titles[1]
    doc = nlp(text)

    for entity in doc.ents:
        print(entity.text, entity.label_)
    
