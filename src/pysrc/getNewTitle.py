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
randomArticle2 = random.choice(articles)
print(randomArticle1.title)
print(randomArticle2.title)

print(Article.combineNounArticlesTitle(randomArticle1, randomArticle2))

sys.stdout.flush()
