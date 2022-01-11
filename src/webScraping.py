import newsAPI
import spacy
from ArticleClass import Article
import random
nlp = spacy.load("en_core_web_sm")



#this headline is not quite right sorta thing where one thing is off for the headline (but it sources that thing from a different headline)
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
            numInstDictNoun[str(chunk.text)] += 1
        except:
            numInstDictNoun[str(chunk.text)] = 1

    numInstDictVerb = {}
    for token in doc:
        if token.pos_ == "VERB":
            try:
                numInstDictVerb[str(token)] += 1
            except:
                numInstDictVerb[str(token)] = 1
    
    numInstDictPerson = {}
    for entity in doc.ents:
        if entity.label_ == "PERSON":
            try:
                numInstDictPerson[str(entity.text)] += 1
            except:
                numInstDictPerson[str(entity.text)] = 1

    return numInstDictNoun, numInstDictVerb, numInstDictPerson

def replacePerson():
    pass
def replaceVerb():
    pass
def replaceNoun():
    pass

# def binarySearch(x, arr):
#     if (x == "it"):
#         print("________" + str(len(arr)) + x)
#     l = 0
#     r = len(arr) - 1
#     while (l <= r):
#         m = l + ((r - l) // 2)
#         if (x == "it"):
#             print(str(l) + "-->" + str(r))

#         if (x == arr[m]):
#             return True
#         elif (x > arr[m]):
#             l = m + 1
#         else:
#             r = m - 1
 
#     return False

# def getLinesOfFile(file):
#     f = open(file, "r")
#     listOfLines = []
#     for line in f:
#         listOfLines.append(line)

#     f.close()
#     return listOfLines


# bannedWords = getLinesOfFile("stopWords.txt")
# def combineDict(*dicts):
#     newDictionary = {}
#     for dictionary in dicts:
#         for key in dictionary.keys():
#             newKey = str(key).lower().strip()
#             if not binarySearch(newKey, bannedWords):
#                 if key in newDictionary:
#                     newDictionary[newKey] = newDictionary[newKey] + dictionary[key]
#                 else:
#                     newDictionary[newKey] = dictionary[key]

#     return newDictionary


if __name__ == "__main__":
    newInstance = WebScraping()
    titles, desc = newInstance.getTitlesAndDesriptions()

    articles = []
    for i in range(len(titles)):
        articles.append(Article(titles[i], desc[i]))
    
    randomArticle1 = random.choice(articles)
    randomArticle2 = random.choice(articles)
    print(randomArticle1)
    print(randomArticle2)
    
    print("Noun Art     : " + Article.combineNounArticlesTitle(randomArticle1, randomArticle2))
    print("Verb Art     : " + Article.combineVerbArticlesTitle(randomArticle1, randomArticle2))
    print("Persons Art  : " + Article.combinePersonsArticlesTitle(randomArticle1, randomArticle2))



    
