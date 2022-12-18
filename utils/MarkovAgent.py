import django
import random
from .markov import MarkovMatrix, ReverseMarkovMatrix

class MarkovAgent:
    def __init__(self, markovMatrix, initState):
        #Params: Markov probability matrix, initial state for agent
        #State is a tuple in the form of (word1, ..., wordn), where n is the state size
        self.markovMatrix = markovMatrix
        self.state = initState
        self.stateSize = markovMatrix.state_size
    
    def transition(self):
        #Transition to a new state using the Markov matrix
        #New state is the old state minus the first word plus the new word
        #e.g. (w1, w2, w3) -> (w2, w3, w4)
        newState = self.state[1:self.stateSize] + (self.markovMatrix.move(self.state), )
    
        self.state = newState
        
    def getState(self):
        #Return current state
        return self.state
        
    def setState(self, state):
        #Param: new state
        #Set agent's current state
        self.state = state
        
    def getLastWord(self):
        return self.state[self.stateSize - 1]
        
    