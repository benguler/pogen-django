import django
import random
import json
import sys
from .PoemUtility import PoemUtility

BEGIN = "___BEGIN__"
END = "___END__"


class MarkovMatrix:
    def __init__(self, corpus, state_size, matrix=None):
        """
        :param corpus: A list of lists, where each outer list is a sentence,
        and each inner list is the words in that sentence.
        :param state_size: The number of items the matrix keeps track of.
        :param matrix: Optional pre-existing probability matrix
        """
        self.corpus = corpus
        self.state_size = state_size
        self.matrix = {}
        if matrix:
            self.matrix = matrix
        else:
            self.train(corpus, state_size)

    def train(self, corpus, state_size):
        """
        :return: A dict of dict, where the keys represent all possible states,
        and point to inner dicts. The inner dicts represent all possible words
        that follow the key state and the amount of times it appears. The first
        key in the matrix will always be ('___BEGIN__', '___BEGIN__').

        Ex. ('___BEGIN__', '___BEGIN__') = {'Farewell': 1, 'I’m': 1}
        Ex. ('Farewell', 'dear'): {'mate,': 1}
        """
        for token in self.corpus:
            key = ([BEGIN] * state_size) + token + [END]
            for i in range(len(token) + 1):
                state = tuple(key[i:i + state_size])
                follow = key[i + state_size]
                if state not in self.matrix:
                    self.matrix[state] = {}

                if follow not in self.matrix[state]:
                    self.matrix[state][follow] = 0

                self.matrix[state][follow] += 1

    def move(self, state):
        """
        :param state: The current state
        :return: The next random word
        """
        freqdict = self.matrix.get(state)
        if freqdict is None:
            return END
        choices = list(freqdict.keys())
        freq = list(freqdict.values())
        freqlist = random.choices(choices, weights=freq, k=sum(freq))

        return random.choice(freqlist)

    def gen(self, init_state=None, iteration=10):
        """
        :param init_state: The first state, default to the naive ___BEGIN___
        :param iteration: How many times the generator yields. Setting this
        to a large number will likely force the generator to stop at ___END___
        """
        state = init_state or (BEGIN,) * self.state_size
        i = iteration
        while i:
            next_word = self.move(state)
            if next_word == END:
                break
            yield next_word
            state = tuple(state[1:]) + (next_word,)
            i -= 1

    def walk(self, init_state=None, iteration=10):
        """
        Return a list representing a single run of the Markov model, either
        starting with a naive BEGIN state, or the provided `init_state`
        (as a tuple).
        """
        return list(self.gen(init_state, iteration))

    def get_matrix(self):
        return self.matrix


class ReverseMarkovMatrix(MarkovMatrix):
    def train(self, corpus, state_size):
        for token in self.corpus:
            token.reverse()
            key = ([BEGIN] * state_size) + token + [END]
            for i in range(len(token) + 1):
                state = tuple(key[i:i + state_size])
                follow = key[i + state_size]
                if state not in self.matrix:
                    self.matrix[state] = {}

                if follow not in self.matrix[state]:
                    self.matrix[state][follow] = 0

                self.matrix[state][follow] += 1