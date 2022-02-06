var article = require('./articleClass')

function getNewTitle(articles){
    var titles = articles[0]
    var desc = articles[1]

    articles = []
    for (let i = 0; i < titles.length; i++) {
        articles.append(new article(titles[i], desc[i]))
    }
    console.log(titles)

    var artNum = Math.random()*articles.length
    var randomArticle1 = articles[artNum]
    articles.pop(artNum)
    artNum = Math.random()*articles.length
    var randomArticle2 = articles[artNum]

    var articleTitle = article.combineNounArticlesTitle(randomArticle1, randomArticle2)

    var newTitle = ""
    for (var word in articleTitle.split(' ')){
        if (word.length > 1){
            newTitle += word.slice(0,1).toUpperCase() + word.slice(1) + " "
        }else{
            newTitle += word.slice(0,1).toUpperCase() + " "
        }
    }

    return randomArticle1.title + "☃" + randomArticle2.title + "☃" + newTitle
}

module.exports = getNewTitle
