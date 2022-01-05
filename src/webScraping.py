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

def getNumInstances(text):
    doc = nlp(text)

    numInstDictNoun = {}
    for chunk in doc.noun_chunks:
        try:
            numInstDictNoun[chunk.text] += 1
        except:
            numInstDictNoun[chunk.text] = 1

    numInstDictVerb = {}
    for token in doc:
        if token.pos_ == "VERB":
            try:
                numInstDictVerb[token] += 1
            except:
                numInstDictVerb[token] = 1
    
    numInstDictPerson = {}
    for entity in doc.ents:
        if entity.label_ == "PERSON":
            try:
                numInstDictPerson[entity.text] += 1
            except:
                numInstDictPerson[entity.text] = 1

    return numInstDictNoun, numInstDictVerb, numInstDictPerson


if __name__ == "__main__":
    newInstance = WebScraping()
    titles, desc = newInstance.getTitlesAndDesriptions()
    firstArt = titles[0] + desc[0]
    secondArt = titles[1] + desc[1]

    firstNoun, firstVerb, firstPerson = getNumInstances(firstArt)
    secNoun, secVerb, secPerson = getNumInstances(secondArt)

    print(secNoun)

    
