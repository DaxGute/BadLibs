var newTitle = require('./getNewTitle')
const fetch = require('node-fetch');

async function getEverything(){
    fetch('https://newsapi.org/v2/top-headlines?country=us&apiKey=45e32894443047b8bde86b7d9ce8720d')
        .then(res => res.json())
        .then((json) => {
            var articleTitles = []
            var articleDesc = []
            for (var article in json.articles){
                article = json.articles[article]
                articleTitles.push(article.title)
                articleDesc.push(article.description)
            }
            console.log(articleTitles)
            return newTitle([articleTitles, articleDesc])
        });
} 


module.exports = getEverything