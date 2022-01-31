import spacy
nlp = spacy.load("en_core_web_sm")

def getLinesOfFile(file):
    f = open(file, "r")
    listOfLines = []
    for line in f:
        listOfLines.append(line)

    f.close()
    return listOfLines

top1000 = getLinesOfFile("src/pysrc/top1000.txt")
top100 = getLinesOfFile("src/pysrc/top100.txt")

def getVerbSentiments():
    f = open("src/pysrc/SentiWords_1.1.txt", "r")
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
        newTitle = ""
        hyphenIndex = -1
        for char in range(len(title)):
            if title[char] == '-':
                hyphenIndex = char        
                self.publisher = title[hyphenIndex+2:]
                newTitle = title[:hyphenIndex-1]

        self.title = newTitle.split("|")[0]

        if description != None:
            combinedText = self.title + ". " + description
        else:
            combinedText = self.title
        self.fullDoc = nlp(combinedText)
        self.Persons = self.getPersons(self.fullDoc)
        self.Nouns = self.getNouns(self.fullDoc)
        self.Verbs = self.getVerbs(self.fullDoc)

        self.titleDoc = nlp(self.title)
        self.titlePersons = self.getPersons(self.titleDoc)
        self.titleNouns = self.getNouns(self.titleDoc)
        self.titleVerbs = self.getVerbs(self.titleDoc)
    
    def __str__(self):
        print("================================")
        print("Article Title: " + self.title)
        print("     Nouns   : " + str(self.Nouns))
        print("     Verbs   : " + str(self.Verbs))
        print("     People  : " + str(self.Persons))
        print("TitleNouns   : " + str(self.titleNouns))
        print("TitleVerbs   : " + str(self.titleVerbs))
        print("TitlePeople  : " + str(self.titlePersons))
        print("================================")
        return ""

    def getNouns(self, doc): # do it based on how common the shared word is 
        """
        First it consolodates the nouns (merges if is duplicate)
        Provides the rules for how each noun should be ranked ranked:
            1) If it is similar to another noun, it either takes on that value or it takes on that noun (I should make more clear)
            2) If the word is greater than 3 words long, it gets points
            3) If each word is not common it gets points 
            4) If the phrase is in the title, it gets points
        """
        numInstDictNoun = {}
        for chunk in doc.noun_chunks:
            currNoun = str(chunk.text).lower()
            calculatedInc = 1
            if str(chunk.text) == self.publisher:
                continue

            toBePopped = []
            for prevNoun in numInstDictNoun.keys(): #checks that there isn't already a similar one
                prevNoun = prevNoun.lower()
                if Article.nounsAreSame(prevNoun, currNoun):

                    if len(currNoun) > len(prevNoun): #this way it always is the largest string
                        calculatedInc += 1 + numInstDictNoun[prevNoun]
                        toBePopped.append(prevNoun)
                    else:
                        currNoun = prevNoun

            for dictKey in toBePopped:
                numInstDictNoun.pop(dictKey)
       
            indivWords = currNoun.split(' ')
            if len(indivWords) >= 3:
                calculatedInc += 0.5
            for i in indivWords:
                if i not in top1000:
                    calculatedInc += 0.25
                    if i in self.title: # is this really neceassary for both nouns and title nouns
                        calculatedInc += 0.5

            try:
                numInstDictNoun[str(currNoun)] += calculatedInc
            except:
                numInstDictNoun[str(currNoun)] = calculatedInc

        return Article.dictToList(numInstDictNoun)



    @staticmethod
    def nounsAreSame(noun1, noun2):
        if noun1 == noun2:  #if they are the same then obviously they are the same
            return True

        firstNoun = noun1.split(" ")
        secondNoun = noun2.split(" ")
        numCounts = 0
        for i in range(len(firstNoun)):
            firstnoun = firstNoun[i]
            for i in range(len(secondNoun)):
                secondnoun = secondNoun[i]
                if secondnoun == firstnoun and firstnoun not in top100:
                    numCounts += 1
        
        if numCounts >= 2: # if they have more than two words in common that aren't super common
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
        if len(article1.titleNouns) < 1 or len(article2.Nouns) < 1:
            return "Not enough nouns mentioned in both articles."
        noun1 = article1.titleNouns[0]
        noun2 = article2.Nouns[0]
        for i in range(len(title)-len(noun1)+1):
            possibleNoun = title[i: i+len(noun1)]
            if possibleNoun.lower() == noun1.lower():
                newArticleTitle = title[:i] + noun2 + title[i+len(noun1):]
                return newArticleTitle
        
        return "I am stupid"
    
    @staticmethod
    def combineVerbArticlesTitle(article1, article2):
        title = article1.title
        if len(article1.titleVerbs) < 1 or len(article2.Verbs) < 1:
            return "Not enough verbs mentioned in both articles."
        verb1 = article1.titleVerbs[0]
        verb2 = article2.Verbs[0]
        for i in range(len(title)-len(verb1)+1):
            possibleNoun = title[i: i+len(verb1)]
            if possibleNoun.lower() == verb1:
                newArticleTitle = title[:i] + verb2 + title[i+len(verb1):]
                return newArticleTitle
    
        return "I am stupid"

    @staticmethod
    def combinePersonsArticlesTitle(article1, article2):
        title = article1.title
        if len(article1.titlePersons) < 1 or len(article2.Persons) < 1:
            return "Not enough people mentioned in both articles."
        person1 = article1.titlePersons[0]
        person2 = article2.Persons[0]
        for i in range(len(title)-len(person1)+1):
            possibleNoun = title[i: i+len(person1)]
            if possibleNoun.lower() == person1.lower():
                newArticleTitle = title[:i] + person2 + title[i+len(person1):]
                return newArticleTitle
        
        return "I am stupid"


    


