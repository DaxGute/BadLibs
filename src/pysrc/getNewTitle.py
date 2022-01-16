from webScraping import WebScraping
from ArticleClass import Article
import random
import sys

newInstance = WebScraping()
titles, desc = newInstance.getTitlesAndDesriptions()

articles = []
for i in range(len(titles)):
    articles.append(Article(titles[i], desc[i]))

randomArticle1 = random.choice(articles)
articles.remove(randomArticle1)
randomArticle2 = random.choice(articles)

articleTitle = Article.combineNounArticlesTitle(randomArticle1, randomArticle2)

newTitle = ""
for word in articleTitle.split(' '):
    newTitle += word.capitalize() + " "

print(randomArticle1.title + "☃" + randomArticle2.title + "☃" + newTitle)

sys.stdout.flush()
