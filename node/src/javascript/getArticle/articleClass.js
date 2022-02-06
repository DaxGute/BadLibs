const spacy = require("spacy");
const fs = require('fs')
const nlp = spacy.load("en_core_web_sm")

// var files = fs.readdirSync('./src/javascript/getArticle/s');
// console.log(files)

var sentiWords = fs.readFileSync('src/javascript/getArticle/sentiWords.txt', 'utf8').split('\n');
var stopWords = fs.readFileSync('./src/javascript/getArticle/stopWords.txt', 'utf8').split('\n');
var top100 = fs.readFileSync('./src/javascript/getArticle/top100.txt', 'utf8').split('\n');
var top1000 = fs.readFileSync('./src/javascript/getArticle/top1000.txt', 'utf8').split('\n');

exports.result = sentiWords

class Article{
    constructor(title, description){
        var newTitle = ""
        var hyphenIndex = -1
        for (let index = 0; index < title.length; index++) {
            var char = title.length
            if (title[char] == '-'){
                hyphenIndex = char        
                this.publisher = title.slice(hyphenIndex+ 2)
                newTitle = title.slice(0, hyphenIndex-1)
            }
        }

        this.title = newTitle.split("|")[0]

        var combinedText = ""
        if (description != undefined){
            combinedText = this.title + ". " + description
        }else{
            combinedText = this.title
        }
        this.fullDoc = nlp(combinedText)
        this.Persons = this.getPersons(this.fullDoc)
        this.Nouns = this.getNouns(this.fullDoc)
        this.Verbs = this.getVerbs(this.fullDoc)

        this.titleDoc = nlp(this.title)
        this.titlePersons = this.getPersons(this.titleDoc)
        this.titleNouns = this.getNouns(this.titleDoc)
        this.titleVerbs = this.getVerbs(this.titleDoc)
    }
    toString(){
        console.log("================================")
        console.log("Article Title: " + this.title)
        console.log("     Nouns   : " + this.Nouns)
        console.log("     Verbs   : " + this.Verbs)
        console.log("     People  : " + this.Persons)
        console.log("TitleNouns   : " + this.titleNouns)
        console.log("TitleVerbs   : " + this.titleVerbs)
        console.log("TitlePeople  : " + this.titlePersons)
        console.log("================================")
        return ""
    }

    getNouns(doc){ // do it based on how common the shared word is 
        /*
        First it consolodates the nouns (merges if is duplicate)
        Provides the rules for how each noun should be ranked ranked:
            1) If it is similar to another noun, it either takes on that value or it takes on that noun (I should make more clear)
            2) If the word is greater than 3 words long, it gets points
            3) If each word is not common it gets points 
            4) If the phrase is in the title, it gets points
        */
        var numInstDictNoun = {}
        for (chunk in doc.noun_chunks){
            var currNoun = str(chunk.text).toLowerCase()
            var calculatedInc = 1
            if (chunk.text.toString() == this.publisher){
                continue
            }

            var toBePopped = []
            for (var prevNoun in Object.keys(numInstDictNoun)){ //checks that there isn't already a similar one
                prevNoun = prevNoun.toLowerCase() //do we have to do this here
                if (Article.nounsAreSame(prevNoun, currNoun)){

                    if (currNoun.length > prevNoun.length){ //this way it always is the largest string
                        calculatedInc += 1 + numInstDictNoun[prevNoun]
                        toBePopped.append(prevNoun)
                    }else{
                        currNoun = prevNoun
                    }
                }
            }

            for (var dictKey in toBePopped){
                numInstDictNoun.pop(dictKey)
            }
       
            indivWords = currNoun.split(' ')
            if (indivWords.length >= 3){
                calculatedInc += 0.5
            }
            for (var i in indivWords){
                if (binarySearch(top1000, i)){
                    calculatedInc += 0.25
                    if (i in this.title){ // is this really neceassary for both nouns and title nouns
                        calculatedInc += 0.5
                    }
                }
            }
            try{
                numInstDictNoun[str(currNoun)] += calculatedInc
            }catch{
                numInstDictNoun[str(currNoun)] = calculatedInc
            }
        }

        return Article.dictToList(numInstDictNoun)

    }

    static dictToList(dict){
        newList = []
        for (var key in Objects.keys(dict)){
            newList.append(key)
        }
        
        Article.mergeSort(newList, dict)
        // print(dict)
        return newList
    }

    static mergeSort(arr, dict){
        if (len(arr) > 1){
            mid = len(arr)//2
            L = arr.slice(0, mid)
            R = arr.slice(mid)
            Article.mergeSort(L, dict)
            Article.mergeSort(R, dict)

            i = j = k = 0
            while (i < L.length && j < R.length){
                if (dict[L[i]] > dict[R[j]]){
                    arr[k] = L[i]
                    i += 1
                } else {
                    arr[k] = R[j]
                    j += 1
                }
                k += 1
            } 

            while (i < L.length){
                arr[k] = L[i]
                i += 1
                k += 1
            }
            while (j < R.length){
                arr[k] = R[j]
                j += 1
                k += 1
            }
        }
    }
    
    static combineNounArticlesTitle(article1, article2){
        console.log("" + article1)
        var title = article1.title
        if (article1.titleNouns.length < 1 || article2.Nouns.length < 1){
            return "Not enough nouns mentioned in both articles."
        }
        var noun1 = article1.titleNouns[0]
        var noun2 = article2.Nouns[0]
        for (let i = 0; i < title.length-noun1.length+1; i++) {
            var possibleNoun = title.slice(i, i+len(noun1))
            if (possibleNoun.toLowerCase() == noun1.toLowerCase()){
                newArticleTitle = title.slice(0, i) + noun2 + title.slice(i+noun1.length)
                return newArticleTitle
            }
        }
        
        return "I am stupid"
    }

    static binarySearch(items, value){
        var startIndex  = 0,
            stopIndex   = items.length - 1,
            middle      = Math.floor((stopIndex + startIndex)/2);
    
        while(items[middle] != value && startIndex < stopIndex){
            if (value < items[middle]){
                stopIndex = middle - 1;
            } else if (value > items[middle]){
                startIndex = middle + 1;
            }
    
            middle = Math.floor((stopIndex + startIndex)/2);
        }
        return (items[middle] != value) ? false: true;
    }
}

module.exports = Article