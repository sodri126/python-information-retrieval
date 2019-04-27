import os
import re

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
            f = open(fullPath, "r+")
            listKorpus[korpus] = f.read()
            f.close()
        return listKorpus

    def __allDocIntoDictionary(self):
        self.__listDoc = {}
        for key, value in self.__processKorpusOneByOne().items():
            self.__listDoc[key] = []
            getAllDoc = re.findall(r"\<DOC\>(.+?)\<\/DOC\>", value.replace("\n", " "))
            for doc in getAllDoc:
                docid = self.__getTextFromTag('DOCID', doc).strip()
                docno = self.__getTextFromTag('DOCNO', doc).strip()
                so = self.__getTextFromTag('SO', doc).strip()
                section = self.__getTextFromTag('SECTION', doc).strip()
                date = self.__getTextFromTag('DATE', doc).strip()
                title = self.__getTextFromTag('TITLE', doc).strip()
                txt = self.__getTextFromTag('TEXT', doc).strip()
                
                self.__listDoc[key].append(dict(DOCID= docid,
                    DOCNO=docno,
                    SO=so,
                    SECTION=section,
                    DATE=date,
                    TITLE=title,
                    TEXT=txt))
    
    def __getTextFromTag(self, tag, txt):
        formatRegex = r'\<{0}\>(.+?)\</{0}\>'.format(tag)
        se = re.search(formatRegex, txt)
        if se:
            return se.group(1)
        else:
            return ""

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
    
    def __answerNumberSix(self):
        totalJakarta = 0
        for key, value in self.__listDoc.items():
            for items in value:
                try:
                    totalJakarta = totalJakarta + items['freqWords']['jakarta']
                except:
                    pass
        print('Berapa kali kata "jakarta" muncul dalam seluruh korpus baik dalam huruf besar maupun kecil? {0} kali'.format(totalJakarta))
    
    def __answerNumberSeven(self):
        totalSentences = 0
        for key, value in self.__listDoc.items():
            for items in value:
                for sentence in items['TEXT'].split('. '):
                    if "metro jaya" in sentence.lower():
                        totalSentences += 1

        print('Berapa jumlah kalimat yang mengandung kata "metro jaya"? {0}'.format(totalSentences))
    
    def __answerNumberEight(self):
        highFreqWords = {}
        for key, value in self.__listDoc.items():
            for items in value:
                for key, value in value['freqWords'].items():
                    

    def answerSectionA(self):
        print("Section A: \n")
        for key, value in self.__listDoc.items():
            print(key)
            self.__answerNumberOne(value)
            self.__answerNumberTwo(value)         
            self.__answerNumberThree(value) 
            self.__answerNumberFour(value) 
            self.__answerNumberFive(value)
    
    def answerSectionB(self):
        print("Section B: \n")
        self.__answerNumberSix()
        self.__answerNumberSeven()
        
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
    
    def __getSentence(self, korpus):
        #st = [sentence for docs in sentences for sentence in docs.split(" ") if re.match("^.*?[a-zA-Z].*?$", sentence)]
        st = []
        allSt = []
        for docs in korpus:
            for sentence in docs['TEXT'].split(". "):
                st.append(sentence)
            allSt.append(st)
            st = []
        
        return allSt

    def __getFreshWordPerKorpus(self):
        for key, value in self.__listDoc.items():
            for items in value:
                words = []
                for word in items['TEXT'].split():
                    wordCleaning = self.__cleanWord(word)
                    if wordCleaning != "":
                        words.append(wordCleaning)
                self.__listDoc[key][value.index(items)]['words'] = words
        
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
    processKorpus.answerSectionB()