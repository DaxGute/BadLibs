import spacy
nlp = spacy.load("en_core_web_sm")

def getLinesOfFile(file):
    f = open(file, "r")
    listOfLines = []
    for line in f:
        listOfLines.append(line)

    f.close()
    return listOfLines

top1000 = getLinesOfFile("top1000.txt")
top100 = getLinesOfFile("top100.txt")

def getVerbSentiments():
    f = open("SentiWords_1.1.txt", "r")
    listOfVerbs = {}
    for line in f:
        if line.find("#v") != -1:
            wordAndValue = line.split("#v")
            word = wordAndValue[0]
            value = float(wordAndValue[1].strip())
            listOfVerbs[word] = value

    f.close()
    return listOfVerbs

verbsSenti = getVerbSentiments()




class Article:
    def __init__(self, title, description):
        hyphenIndex = -1
        for char in range(len(title)):
            if title[char] == '-':
                hyphenIndex = char
                        
        self.publisher = title[hyphenIndex+1:]
        title = title[:hyphenIndex-1]

        self.getDoc(title, description)
        self.title = title
        self.Persons = self.getPersons(self.doc)
        self.Nouns = self.getNouns(self.doc)
        self.Verbs = self.getVerbs(self.doc)
        doc = nlp(title)
        self.titlePersons = self.getPersons(doc)
        self.titleNouns = self.getNouns(doc)
        self.titleVerbs = self.getVerbs(doc)
    
    def __str__(self):
        print("================================")
        print("Article Title: " + self.title)
        print("     Nouns   : " + str(self.Nouns))
        print("     Verbs   : " + str(self.Verbs))
        print("     People  : " + str(self.Persons))
        print("================================")
        return ""

    def getDoc(self, title, description):
        if description != None:
            combinedText = title + ". " + description
        else:
            combinedText = title
        self.doc = nlp(combinedText)

    def getNouns(self, doc): # do it based on how common the shared word is 
        numInstDictNoun = {}
        for chunk in doc.noun_chunks: #do prepoccessing to get rid of the news station
            if chunk.text not in self.Persons:
                text = chunk.text
                for person in numInstDictNoun.keys():
                    if Article.getNounSimilarity(person.lower(), str(chunk.text.lower())):
                        text = person

                calculatedInc = 1
                if len(text) >= 3:
                    calculatedInc += 0.5
                for i in text.split(" "):
                    if i not in top1000:
                        calculatedInc += 0.25
                if chunk.text in self.title:
                    calculatedInc += 0.5

                try:
                    numInstDictNoun[str(text)] += calculatedInc
                except:
                    numInstDictNoun[str(text)] = calculatedInc

        return Article.dictToList(numInstDictNoun)

    @staticmethod
    def getNounSimilarity(noun1, noun2):
        firstNoun = noun1.split(" ")
        secondNoun = noun2.split(" ")
        numCounts = 0
        for i in range(len(firstNoun)):
            firstnoun = firstNoun[i]
            for i in range(len(secondNoun)):
                secondnoun = secondNoun[i]
                if secondnoun == firstnoun and firstnoun:
                    numCounts += 1
        
        if numCounts >= 2:
            return True
        return False

    def getVerbs(self, doc): # do it based on the sentiment
        numInstDictVerb = {}
        for token in doc:
            if token.pos_ == "VERB":
                text = str(token).lower()

                calculatedInc = 1
                if text in verbsSenti:
                    calculatedInc += abs(verbsSenti[text] * 5)
                if text not in top100:
                    if text not in top1000:
                        calculatedInc += 1
                    else:
                        calculatedInc = 0.25
                else:
                    calculatedInc = 0

                try:
                    numInstDictVerb[text] += calculatedInc
                except:
                    numInstDictVerb[text] = calculatedInc

        return Article.dictToList(numInstDictVerb)

    def getPersons(self, doc): # do it based on how much it has in common
        numInstDictPerson = {}
        for entity in doc.ents:
            if entity.label_ == "PERSON":
                text = entity.text
                for person in numInstDictPerson.keys():
                    if Article.getPersonSimilarity(person, str(entity.text)):
                        text = person
                
                try:
                    numInstDictPerson[str(text)] += 1
                except:
                    numInstDictPerson[str(text)] = 1

        return Article.dictToList(numInstDictPerson)

    @staticmethod
    def getPersonSimilarity(name1, name2):
        firstName = name1.split(" ")
        secondName = name2.split(" ")
        if len(firstName) >= 2 and len(secondName) >= 2:
            for i in range(len(firstName)-1):
                firstname = firstName[i] + " " + firstName[i+1]
                for i in range(len(secondName)-1):
                    secondname = secondName[i] + " " + secondName[i+1]
                    if secondname == firstname:
                        return True
        
        return False
    @staticmethod
    def dictToList(dict):
        newList = []
        for key, value in dict.items():
            newList.append(key)
        
        Article.mergeSort(newList, dict)
        # print(dict)
        return newList

    @staticmethod
    def mergeSort(arr, dict):
        if len(arr) > 1:
            mid = len(arr)//2
            L = arr[:mid]
            R = arr[mid:]
            Article.mergeSort(L, dict)
            Article.mergeSort(R, dict)

            i = j = k = 0
            while i < len(L) and j < len(R):
                if dict[L[i]] > dict[R[j]]:
                    arr[k] = L[i]
                    i += 1
                else:
                    arr[k] = R[j]
                    j += 1
                k += 1

            while i < len(L):
                arr[k] = L[i]
                i += 1
                k += 1
            while j < len(R):
                arr[k] = R[j]
                j += 1
                k += 1
    
    @staticmethod
    def combineNounArticlesTitle(article1, article2):
        title = article1.title
        if len(article1.Nouns) < 1 or len(article2.Nouns) < 1:
            return "Not enough nouns mentioned in both articles."
        noun1 = article1.titleNouns[0]
        noun2 = article2.Nouns[0]
        for i in range(len(title)-len(noun1)):
            possibleNoun = title[i: i+len(noun1)]
            if possibleNoun.lower() == noun1.lower():
                newArticleTitle = title[:i] + noun2 + title[i+len(noun1):]
                return newArticleTitle
        
        return "I am stupid"
    
    @staticmethod
    def combineVerbArticlesTitle(article1, article2):
        title = article1.title
        if len(article1.Verbs) < 1 or len(article2.Verbs) < 1:
            return "Not enough verbs mentioned in both articles."
        verb1 = article1.titleVerbs[0]
        verb2 = article2.Verbs[0]
        for i in range(len(title)-len(verb1)):
            possibleNoun = title[i: i+len(verb1)]
            if possibleNoun.lower() == verb1:
                newArticleTitle = title[:i] + verb2 + title[i+len(verb1):]
                return newArticleTitle
    
        return "I am stupid"

    @staticmethod
    def combinePersonsArticlesTitle(article1, article2):
        title = article1.title
        if len(article1.Persons) < 1 or len(article2.Persons) < 1:
            return "Not enough people mentioned in both articles."
        person1 = article1.titlePersons[0]
        person2 = article2.Persons[0]
        for i in range(len(title)-len(person1)):
            possibleNoun = title[i: i+len(person1)]
            if possibleNoun.lower() == person1.lower():
                newArticleTitle = title[:i] + person2 + title[i+len(person1):]
                return newArticleTitle
        
        return "I am stupid"


    


