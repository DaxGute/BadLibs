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
        text = self.combineText(title, description)
        self.doc = nlp(text)

        self.Persons= self.getPersons()    
        self.Nouns= self.getNouns()
        self.Verbs= self.getVerbs()

    def combineText(self, title, description):
        return title + ". " + description

    def getNouns(self): # do it based on how common the shared word is 
        numInstDictNoun = {}
        for chunk in self.doc.noun_chunks: #do prepoccessing to get rid of the news station
            if chunk.text not in self.Persons:
                text = chunk.text
                for person in numInstDictNoun.keys():
                    if self.getPersonSimilarity(person.lower(), str(chunk.text.lower())):
                        text = person

                calculatedInc = 1
                if len(text) >= 3:
                    calculatedInc += 0.5
                for i in text.split(" "):
                    if i not in top1000:
                        calculatedInc += 0.25

                try:
                    numInstDictNoun[str(text)] += calculatedInc
                except:
                    numInstDictNoun[str(text)] = calculatedInc

        return Article.dictToList(numInstDictNoun)

    def getNounSimilarity(self, noun1, noun2):
        firstNoun = noun1.split(" ")
        secondNoun = noun2.split(" ")
        if len(firstNoun) >= 2 and len(secondNoun) >= 2:
            for i in range(len(firstNoun)-1):
                firstname = firstNoun[i] + " " + firstNoun[i+1]
                for i in range(len(secondNoun)-1):
                    secondname = secondNoun[i] + " " + secondNoun[i+1]
                    if secondname == firstname and firstname[0] not in top100 and firstname[1] not in top100:
                        return True
        
        return 0

    def getVerbs(self): # do it based on the sentiment
        numInstDictVerb = {}
        for token in self.doc:
            if token.pos_ == "VERB":
                text = str(token).lower()

                calculatedInc = 1
                if text in verbsSenti:
                    calculatedInc += abs(verbsSenti[text] * 10)

                try:
                    numInstDictVerb[str(token)] += calculatedInc
                except:
                    numInstDictVerb[str(token)] = calculatedInc

        return Article.dictToList(numInstDictVerb)

    def getPersons(self): # do it based on how much it has in common
        numInstDictPerson = {}
        for entity in self.doc.ents:
            if entity.label_ == "PERSON":
                text = entity.text
                for person in numInstDictPerson.keys():
                    if self.getPersonSimilarity(person, str(entity.text)):
                        text = person
                
                try:
                    numInstDictPerson[str(text)] += 1
                except:
                    numInstDictPerson[str(text)] = 1

        return Article.dictToList(numInstDictPerson)

    def getPersonSimilarity(self, name1, name2):
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
        

