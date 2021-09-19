import enum
from enum import Enum

landa1 = 0.01
landa2 = 0.09
landa3 = 0.9
epsilon = 0.01

unigram = 0
bigram = 1
test = 2


def read(path, model):
    file = open(path, "r", encoding='UTF-8')
    f = dict()
    if model == test:
        while True:
            fs = file.readline()
            if len(fs) == 0:
                break
            split = fs.split("\t")

            p = "<s> " + split[1][:-1] + " </s>"
            f[p] = int(split[0])
        return f
    elif model == unigram:
        while True:
            fs = file.readline()
            if len(fs) == 0:
                break
            fs = fs[:-1]
            fs = "<s> " + fs + " </s>"
            words = fs.split()
            for word in words:
                f[word] = f.get(word, 0) + 1
        return f

    elif model == bigram:
        while True:
            fs = file.readline()
            if len(fs) == 0:
                break
            fs = fs[:-1]
            fs = "<s> " + fs + " </s>"
            words = fs.split()
            preWord = None
            for word in words:
                if preWord is not None:
                    f[(preWord, word)] = f.get((preWord, word), 0) + 1
                preWord = word
        return f


class Bigram:
    def __init__(self, path):
        self.unidictionary = {key: val for key, val in read(path, unigram).items() if val > 0}
        self.Bidictionary = {key: val for key, val in read(path, bigram).items() if val > 0}
        self.eachWordSize = len(self.unidictionary)
        self.totallSize = sum(self.unidictionary.values())

    def uni_word(self, word):
        wordNo = self.unidictionary.get(word, 0)
        probability = float(wordNo) / float(
            self.totallSize - self.unidictionary.get("<s>") - self.unidictionary.get("</s>"))
        if wordNo == 0 or self.totallSize == 0:
            return 0
        else:
            return probability


    def bi_word(self, preWord, word):
        WordsNo = self.Bidictionary.get((preWord, word), 0)
        WordNo = self.unidictionary.get(preWord, 0)
        if WordsNo == 0 or self.unidictionary.get(word, 0) == 0:
            return 0
        return float(WordsNo) / float(WordNo)

    def backOffSentenceProb(self, sentence):
        sentence = "<s> " + sentence + " </s>"
        words = sentence.split(" ")
        preWord = None
        back_off_sentence_probability = float(1)
        for word in words:
            if preWord is not None:
                back_off_word_probability = (self.bi_word(preWord, word) * landa3) + (self.uni_word(word) * landa2) + (
                        landa1 * epsilon)
                back_off_sentence_probability *= back_off_word_probability
            preWord = word
        return back_off_sentence_probability




testSet = read("./test_set/test3.txt", test)
Ferdowsy = Bigram("./train_set/ferdowsi_train.txt")
Hafez = Bigram("./train_set/hafez_train.txt")
Molavy = Bigram("./train_set/molavi_train.txt")

rightAnswer = 0
for key, value in testSet.items():
    ferdowsiProbability = Ferdowsy.backOffSentenceProb(key)
    hafezProbability = Hafez.backOffSentenceProb(key)
    molaviProbability = Molavy.backOffSentenceProb(key)
    maxProbability = max(ferdowsiProbability, hafezProbability, molaviProbability)
    if maxProbability == ferdowsiProbability:
        answer = 1
    elif maxProbability == hafezProbability:
        answer = 2
    elif maxProbability == molaviProbability:
        answer = 3
    if answer == value:
        rightAnswer += 1
print(str(rightAnswer) + " Were Correct Answers ")
precision = rightAnswer / len(testSet)
print(str(precision) + " precision ")
