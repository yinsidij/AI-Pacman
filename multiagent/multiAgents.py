# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

import sys
from random import randint
class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
		
        "*** YOUR CODE HERE ***"
        newGhostPos = successorGameState.getGhostPosition(1);
        

        WEIGHT_FOOD = 10.0
        WEIGHT_GHOST = 10.0

        value = successorGameState.getScore()

        distanceToGhost = manhattanDistance(newPos, newGhostPos)
        if distanceToGhost > 0:
            value -= WEIGHT_GHOST / distanceToGhost
			
        #print "========================="
        #for x in newFood.asList():
		#    print x
        #print "========================="	
        
        distancesToFood = [manhattanDistance(newPos, x) for x in newFood.asList()]
        if len(distancesToFood):
            value += WEIGHT_FOOD / min(distancesToFood)
        #
        return value

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        ret = self.value(gameState, 0, 0)
        return ret[0]
		
    def value(self, gameState, index, depth):
    
        if (index >= gameState.getNumAgents()):
            index = 0
            depth=depth+1
            
        if (depth == self.depth):
            return ("", self.evaluationFunction(gameState))
            
        if (index == 0):
            pair = ("unknown", -sys.maxint-1)
            legal = gameState.getLegalActions(0)
            if not legal:
                return ("", self.evaluationFunction(gameState))
            for action in legal:
                ret = self.value(gameState.generateSuccessor(0, action), 1, depth)
                if (ret[1]>pair[1]):
                    pair=(action, ret[1])

            return pair            
        else:
            pair = ("unknown", sys.maxint)
            legal = gameState.getLegalActions(index)
            if not legal:
                return ("", self.evaluationFunction(gameState))        
            
            for action in legal:
                ret = self.value(gameState.generateSuccessor(index, action), index + 1, depth)
                if (ret[1]<pair[1]):
                    pair=(action, ret[1])
            
            return pair

       
                    



    
        
	
class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        alpha = -1-sys.maxint
        beta = sys.maxint
        return self.value(gameState, 0, 0, alpha, beta)[0]
    def value(self, gameState, index, depth, alpha, beta):
    
        if (index >= gameState.getNumAgents()):
            index = 0
            depth=depth+1
            
        if (depth == self.depth):
            return ("", self.evaluationFunction(gameState))
            
        if (index == 0):
            pair = ("unknown", -sys.maxint-1)
            legal = gameState.getLegalActions(0)
            if not legal:
                return ("", self.evaluationFunction(gameState))
            for action in legal:
                ret = self.value(gameState.generateSuccessor(0, action), 1, depth, alpha, beta)
                if (ret[1]>pair[1]):
                    pair=(action, ret[1])
                if (pair[1]>beta):
                    return pair
                alpha=max(alpha, pair[1])

            return pair            
        else:
            pair = ("unknown", sys.maxint)
            legal = gameState.getLegalActions(index)
            if not legal:
                return ("", self.evaluationFunction(gameState))        
            
            for action in legal:
                ret = self.value(gameState.generateSuccessor(index, action), index + 1, depth, alpha, beta)
                if (ret[1]<pair[1]):
                    pair=(action, ret[1])
                if (pair[1]<alpha):
                    return pair
                beta = min(beta, pair[1])
            return pair

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        return self.value(gameState, 0, 0)[0]
        
    def value(self, gameState, index, depth):
    
        if (index >= gameState.getNumAgents()):
            index = 0
            depth=depth+1
            
        if (depth == self.depth):
            return ("", self.evaluationFunction(gameState))
            
        if (index == 0):
            pair = ("unknown", -sys.maxint-1)
            legal = gameState.getLegalActions(0)
            if not legal:
                return ("", self.evaluationFunction(gameState))
            for action in legal:
                ret = self.value(gameState.generateSuccessor(0, action), 1, depth)
                if (ret[1]>pair[1]):
                    pair=(action, ret[1])

            return pair            
        else:
            pair = ("unknown", sys.maxint)
            legal = gameState.getLegalActions(index)
            if not legal:
                return ("", self.evaluationFunction(gameState)) 
            
            expectvalue = 0
            #print "====================legal's length = ", len(legal)
            for action in legal:
                ret = self.value(gameState.generateSuccessor(index, action), index+1, depth)
                expectvalue+= 1.0/len(legal) * ret[1]
            
            pair = (random.choice(legal), expectvalue)
            return pair              

            
            

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    pacmanPos = currentGameState.getPacmanPosition()
    ghostPos = currentGameState.getGhostPositions()
    food = currentGameState.getFood()
    value = 0
    
    
    distToGhost = sys.maxint
    for pos in ghostPos:
        distToGhos = min(distToGhost, manhattanDistance(pacmanPos, pos))
    
    distToFood = [manhattanDistance(pacmanPos, x) for x in food.asList()]
    
    WEIGHT_FOOD = 20.0
    WEIGHT_GHOST = 1.0

    #print "distToGhos= ", distToGhos
    #print "min(distToFood)= ", min(distToFood)
    #if distToGhos > 0:
    #    value -= WEIGHT_GHOST * distToGhos 

    if len(distToFood):
        #print "min(distToFood)= ", min(distToFood)
        value += WEIGHT_FOOD / min(distToFood)
        value += 100/len(distToFood)
    else:
        value += 1000
    
    
    value = value + currentGameState.getScore()
    return value

# Abbreviation
better = betterEvaluationFunction

