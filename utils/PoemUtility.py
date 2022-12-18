"""
PoemUtility.py
Contributors - Alex Castro

This python script contains three important functionality

1- Opens a csv file for reading and uses TextBlob to tokenize each sentence into a nested list of words

2- Classify poems using the TextBlob Naive-Bayes classifier.

3- Calculate the probability distance that the sentence belongs to the given poem category

4- Helper method to remove punctuation from a string



"""
# need to install punkt manually by "nltk.download('punkt')"
import django
import csv
import nltk
from nltk.tokenize import word_tokenize
from nltk.tokenize import RegexpTokenizer 
from textblob import TextBlob
from .classifiers import NaiveBayesClassifier


class PoemUtility:

    @staticmethod
    def tokenize(filename):
        tk = RegexpTokenizer("[\\w+']+|[^\\w\\s]+")
        try:
            matrix = []
            with open ('CSVs/'+filename, 'r') as csvfile:
                csv_reader = csv.reader(csvfile)
                for line in csv_reader:
                    poem_sentence = line[0]
                    poem_sentence = removePunctuation(poem_sentence)
                    data = tk.tokenize(poem_sentence)
                    matrix.append(data)
            return matrix
        except IOError:
            print ('\nFile not found in tokenize() method')
    
    
    @staticmethod
    def classifyPoems(filename):
        try:
            with open('CSVs/'+filename, 'r') as fp:
                print('opened ' + filename )
                global cl
                cl = NaiveBayesClassifier(fp, format="csv")
                print(cl)
        except IOError:
            print('\nFile not found for Naive-Bayes Classifier')
            

    @staticmethod
    def classifySentence(sentence, category):
        prob_dist = cl.prob_classify(sentence)
        return round(prob_dist.prob(category),2)


def removePunctuation(my_str):
    # define punctuation
    punctuations = '''!()-[]{};:"\,<>./?@#$%^&*_~'''

    mydot = "."

    # remove punctuation from the string
    no_punct = ""
    for char in my_str:
        if char == mydot:
            no_punct = no_punct + " "
        if char not in punctuations:
            no_punct = no_punct + char
            
    # display the unpunctuated string
    #print(no_punct)
    return no_punct           
        
