from .markov import MarkovMatrix
from .MarkovAgent import MarkovAgent
from .PoemUtility import PoemUtility
from .Poem import Poem

def genPoem(genre, strSyls):
    category = genre
    corpus = PoemUtility.tokenize(category + '.csv')
    matrix = MarkovMatrix(corpus, 2)


    syls = []
    syl = ""
    
    digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

    for i in range (len(strSyls)):
        c = strSyls[i]

        if c == '-':
            syls += [int(syl)]
            syl = ""

        elif c in digits:
            syl += c

        if i == len(strSyls) - 1 and len(syl) != 0:
            syls += [int(syl)]

    poeminstance = Poem(matrix, syls, category, True)
    return poeminstance.generatePoem()
    
    
