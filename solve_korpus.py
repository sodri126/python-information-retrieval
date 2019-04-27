from bs4 import BeautifulSoup
import os
from nltk.tokenize import sent_tokenize
import re
import nltk

#te
class ProcessKorpus:
    def __init__(self, fileDirectory):
        self.__fileDirectory = fileDirectory
        self.__allDocIntoDictionary()
        self.__getFreshWordPerKorpus()
        self.__frequentWords()

    def __processKorpusOneByOne(self):
        listKorpus = {}
        for korpus in os.listdir(self.__fileDirectory):
            fullPath = self.__fileDirectory + korpus
            with open(fullPath, "r") as f:
                xmlstr = "<root>{0}</root>".format(f.read())
                xmlObject = BeautifulSoup(xmlstr, "xml")
            
            listKorpus[korpus] = xmlObject
        return listKorpus
    
    def __allDocIntoDictionary(self):
        self.__listDoc = {}
        for key, value in self.__processKorpusOneByOne().items():
            self.__listDoc[key] = []
            for tag in value.find_all('DOC'):
                txtClean = str(tag.TEXT).replace("<TEXT>", "").replace("</TEXT>", "").replace("\n", " ").strip()
                self.__listDoc[key].append(dict(DOCID= tag.DOCID.text.strip(),
                        DOCNO=tag.DOCNO.text.strip(),
                        SO=tag.SO.text.strip(),
                        SECTION=tag.SECTION.text.strip(),
                        DATE=tag.DATE.text.strip(),
                        TITLE=tag.TITLE.text.strip(),
                        TEXT=txtClean))

    def __answerNumberOne(self, korpus):
        totalDoc = len(korpus)
        print("Berapa jumlah dokumen berita pada korpus? {0} dokumen".format(totalDoc))
        #count all DOC KORPUS A,B,C and D
    
    def __answerNumberTwo(self, korpus):
        sentences = self.__getSentence(korpus)  
        totalSentences = list(map(lambda s: len(s), sentences))
        averageSentences = sum(totalSentences) / len(totalSentences)      
        print("Berapa jumlah kalimat rata-rata untuk setiap dokumen berita pada korpus? {0}".format(averageSentences))
    
    def __answerNumberThree(self, korpus):
        #totalUniqueWords = len(list(filter(lambda value: value['freqWords'][1] == 1, korpus)))
        totalUniqueWords = 0
        for items in korpus:
            for key, value in items['freqWords'].items():
                if value == 1:
                    totalUniqueWords += 1
        print("Berapa jumlah kata unik yang terdapat dalam korpus? {0}".format(totalUniqueWords))
    
    def __answerNumberFour(self, korpus):
        totalWords = [value for items in korpus for key, value in items['freqWords'].items()]
        averageWords = sum(totalWords) / len(totalWords)
        print("Berapa rata-rata frekuensi kata dari setiap dokumen berita pada korpus? {0}".format(averageWords))
    
    def __answerNumberFive(self, korpus):
        totalMoreThanTwoWords = 0
        for items in korpus:
            for key, value in items['freqWords'].items():
                if value > 1:
                    totalMoreThanTwoWords += 1
        print("Ada berapa jumlah kata yang memiliki frekuensi lebih dari 1 dalam korpus? {0}".format(totalMoreThanTwoWords))
    
    def answerSectionA(self):
        for key, value in self.__listDoc.items():
            print(key)
            self.__answerNumberOne(value)
            self.__answerNumberTwo(value)         
            self.__answerNumberThree(value) 
            self.__answerNumberFour(value) 
            self.__answerNumberFive(value)
    
    def __getSentence(self, sentences):
        #st = [sentence for docs in sentences for sentence in docs.split(" ") if re.match("^.*?[a-zA-Z].*?$", sentence)]
        st = []
        allSt = []
        for docs in sentences:
            for sentence in docs['TEXT'].split(". "):
                if re.match("^.*?[a-zA-Z].*?$", sentence):
                    st.append(sentence)
            allSt.append(st)
            st = []
        
        return allSt
    
    def __cleanWord(self, word):
        if word == "":
            return word

        if (re.match("^[0-9]$", word)):
            word = ""
            return self.__cleanWord(word)

        if (not re.match("^([a-zA-Z]).*?[a-zA-Z].*?$", word)):
            word = word.replace(word[0], "")
            return self.__cleanWord(word)

        if (not re.match("^[a-zA-Z].*?([a-zA-Z])$", word)):
            word = word.replace(word[len(word)-1], "")
            return self.__cleanWord(word)
            
        return word.lower()
    
    def __getFreshWordPerKorpus(self):
        for key, value in self.__listDoc.items():
            for items in value:
                words = []
                for word in items['TEXT'].split():
                    wordCleaning = self.__cleanWord(word)
                    if wordCleaning != "":
                        words.append(wordCleaning)
                self.__listDoc[key][value.index(items)]['words'] = words
    
    def __insert(self, source_str, insert_str, pos):
        return source_str[:pos] + insert_str + source_str[pos:]
    
    def __frequentWords(self):
        for key, value in self.__listDoc.items():
            for items in value:
                freqWords = {}
                for word in items['words']:
                    if word in freqWords:
                        freqWords[word] += 1
                    else:
                        freqWords[word] = 1
                self.__listDoc[key][value.index(items)]['freqWords'] = freqWords


if __name__ == "__main__":
    processKorpus = ProcessKorpus("korpus/")
    processKorpus.answerSectionA()
    #print(processKorpus.allDocIntoDictionary())
    #processKorpus.answerEachKorpus()