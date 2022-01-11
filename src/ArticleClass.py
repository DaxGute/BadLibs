import spacy
nlp = spacy.load("en_core_web_sm")

class Article:
    def __init__(self, title, description):
        text = self.combineText(title, description)
        self.doc = nlp(text)

        self.Nouns= self.getNouns()
        self.Verbs= self.getVerbs()
        self.Persons= self.getPersons()    

    def combineText(self, title, description):
        return title + ". " + description

    def getNouns(self):
        numInstDictNoun = {}
        for chunk in self.doc.noun_chunks:
            try:
                numInstDictNoun[str(chunk.text)] += 1
            except:
                numInstDictNoun[str(chunk.text)] = 1

        return Article.dictToList(numInstDictNoun)

    def getVerbs(self):
        numInstDictVerb = {}
        for token in self.doc:
            if token.pos_ == "VERB":
                try:
                    numInstDictVerb[str(token)] += 1
                except:
                    numInstDictVerb[str(token)] = 1

        return Article.dictToList(numInstDictVerb)

    def getPersons(self):
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
        print(dict)
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
                if dict[L[i]] < dict[R[j]]:
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
        

