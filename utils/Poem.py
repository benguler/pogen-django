import django
from .MarkovAgent import MarkovAgent
from .markov import MarkovMatrix, ReverseMarkovMatrix
from .PoemUtility import PoemUtility
import syllables

BEGIN = "___BEGIN__"
END = "___END__"


class Poem:
    def __init__(self, markovMatrix, numSyls, category, sBool):
        # params: markov probability matrix, number of syllables per line, category of poem (period_genre), bool that dictates if poem will have explicit syllable count
        self.markovMatrix = markovMatrix
        self.numSyls = numSyls
        self.category = category
        self.sBool = sBool  # True for explicit syllable count (line must have exactly n syllables) false for maximum syllable count (line may have at most n syllables)

    def generatePoem(self):
        # Generate poem given specifications in constructor
        agent = MarkovAgent(self.markovMatrix, self.genSeed())  # Create agent with poem seed as initial state
        poem = ""
        lines = []
        prevLines = []

        # For each line of the poem
        for syln in self.numSyls:
            score = 0

            minscore = 0.7
            iterations = 0
            # Generate line for poem and run nb classification until nb score is enough
            while (score < minscore):
                line = ""

                sylCount = 0

                # Add initial state to poem (the seed), minus the last word of that state
                for i in range(agent.stateSize - 1):
                    line += agent.getState()[i] + " "
                    sylCount += syllables.estimate(agent.getState()[i])

                # Generate line with roughly correct number of syllables
                # agent.getLastWord() == END) implies line is finished

                # Runs while sylcount is not equal to required syllable count for line (or when sylcount is not <= syllable count when sBool is false) and end of line has not been reached
                # Lines must go from BEGIN to END
                while (not ((sylCount == syln if self.sBool else sylCount <= syln) and agent.getLastWord() == END)):
                    if (sylCount > syln or (
                    agent.getLastWord() == END if self.sBool else False)):  # If number of syllables has been surpassed or finished line has too few syllables (only when syllables count has no min, i.e sBool = false)
                        # Restart with new line with new seed
                        agent.setState(self.genSeed())

                        line = ""

                        sylCount = 0

                        for i in range(agent.stateSize - 1):
                            line += agent.getState()[i] + " "
                            sylCount += syllables.estimate(agent.getState()[i])

                    line += agent.getLastWord() + " "  # Add the last word of the agent's current state to the line
                    sylCount += syllables.estimate(agent.getLastWord())  # Update overall syllable count

                    agent.transition()  # Have the agent transition to a new state

                if (line not in prevLines):
                    score = self.nbDist(line)
                   
                    prevLines += [line]

                else:
                    score = 0
                    
                agent.setState(self.genSeed())  # Initialize agent state to new seed for next line/round of nb classification

                
                iterations += 1
                if(iterations > 10):
                    if minscore >= 0.3:
                        minscore -= 0.1
                    iterations = 0

            lines += [line]

        return lines

    def genSeed(self):
        # Generate initial n words of the poem
        seed = tuple(self.markovMatrix.walk(None, self.markovMatrix.state_size))

        if (len(seed) != self.markovMatrix.state_size):  # If seed is wrong state size
            return self.genSeed()  # Retry

        return seed

    def nbDist(self, line):
        # param: line to run Naive-Bayes classification on
        # Get NaiveBayes probability distribution for category
        return PoemUtility.classifySentence(line, self.category)

        # Return 0 when not testing nb classification. Training takes too long
        return 0