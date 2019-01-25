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
        foodList = successorGameState.getFood().asList()

        closestGhost = 11111
        for gh in newGhostStates:
          i = util.manhattanDistance(newPos, gh.getPosition())
          if i < closestGhost:
            closestGhost = i
                
        if closestGhost == 0:
          return -11111

        closestFood = 11111
        for f in foodList:
          i = util.manhattanDistance(newPos, f)
          if (i < closestFood) and i != 0:
            closestFood = i

        if (currentGameState.getNumFood() > successorGameState.getNumFood()):
          closestFood = closestFood / 4.0

        return successorGameState.getScore() + closestGhost/closestFood				#the biggest the distance to the ghosts the better, and the lesser the distance to food the better

        

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
        results = []
        def minimax(gameState, i):
        	agents = gameState.getNumAgents()

        	#testing if it is a terminal case
        	if gameState.isWin() or gameState.isLose() or i >= self.depth*agents:
        		return self.evaluationFunction(gameState)

        	if ((i % agents) == 0):
        		#we are in the max agent, aka the pacman
        		legalActions = gameState.getLegalActions(0)

        		v = -float('inf')		#setting it negative infinity

        		for action in legalActions:
        			#using the agent 0
        			v = max(v, minimax((gameState.generateSuccessor(0, action)), i + 1))
        			if i == 0:
        				results.append(v)
        		return v
        	else:
        		#here is where the ghosts are playing
        		legalActions = gameState.getLegalActions(i % agents)

        		v = float('inf')		#setting it to infinity

        		for action in legalActions:
        			#using the agent i % agents
        			v = min(v, minimax((gameState.generateSuccessor(i % agents, action)), i + 1))
        		return v

        #starting with the pacman man
        minimax(gameState, 0)

        a = gameState.getLegalActions(0)

        #this is the value that interests the pacman
        maximum = max(results)

        return a[results.index(maximum)]
        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        results = []
        def alphabeta(gameState, i, a, b):
        	agents = gameState.getNumAgents()

        	#testing if it is a terminal case
        	if gameState.isWin() or gameState.isLose() or i >= self.depth*agents:
        		return self.evaluationFunction(gameState)

        	if ((i % agents) == 0):
        		#it's the pacman's turn
        		legalActions = gameState.getLegalActions(0)

        		v = -float('inf')		#setting it negative infinity

        		for action in legalActions:
        			v = max(v, alphabeta((gameState.generateSuccessor(0, action)), i + 1, a, b))
        			if i == 0:
        				results.append(v)
        			if v > b:
        				break
        			a = max(a, v)
        		return v
        	else:
        		#a ghost is playing
        		legalActions = gameState.getLegalActions(i % agents)

        		v = float('inf')		#setting it to infinity

        		for action in legalActions:
        			v = min(v, alphabeta((gameState.generateSuccessor(i % agents, action)), i + 1, a, b))
        			if a > v:
        				break
        			b = min(b, v)
        		return v

        neg_inf = -float('inf')
        pos_inf = float('inf')

        alphabeta(gameState, 0, neg_inf, pos_inf)


        a = gameState.getLegalActions(0)

        #this is the value that interests the pacman
        maximum = max(results)

        return a[results.index(maximum)]
        util.raiseNotDefined()

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

        results = []
        def expectimax(gameState, i):
        	agents = gameState.getNumAgents()

        	#testing if it is a terminal case
        	if gameState.isWin() or gameState.isLose() or i >= self.depth*agents:
        		return self.evaluationFunction(gameState)

        	if ((i % agents) == 0):
        		#max agent is playing now
        		legalActions = gameState.getLegalActions(0)

        		v = -float('inf')

        		for action in legalActions:
        			v = max(v, expectimax((gameState.generateSuccessor(0, action)), i + 1))
        			if i == 0:
        				results.append(v)

        		return v
        	else:
        		#time for the ghosts to play
        		v = 0
        		g = 0

        		legalActions = gameState.getLegalActions(i % agents)

        		for action in legalActions:
        			v = v + expectimax(gameState.generateSuccessor(i % agents, action), i + 1)
        			g = g + 1

        		if (g != 0):
        			v = v/(g * 1.0)
        		else:
        			v = 0

        		return v

        expectimax(gameState, 0)

        a = gameState.getLegalActions(0)

        #this is the value that interests the pacman
        maximum = max(results)

        return a[results.index(maximum)]

        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"

    pos = currentGameState.getPacmanPosition()

    #current score
    score = currentGameState.getScore()

    #calculating the distance of the pacman to the capsules
    capsules = currentGameState.getCapsules()

    if len(capsules) != 0:
    	score = score - (30 * len(capsules))

    #calculating the distance of the pacman to the food dots
    food_distance = []
    for f in (currentGameState.getFood().asList()):
    	dist = util.manhattanDistance(pos, f)
    	food_distance.append(dist)

    if len(food_distance) != 0:
    	score = score - (2 * min(food_distance)) - (8 * len(food_distance))

    ghostStates = currentGameState.getGhostStates()

    scared_distance = []
    ghost_distance = []
    for ghostState in ghostStates:
    	if ghostState.scaredTimer != 0:
    		#dealing with the scared ghosts
    		dist = util.manhattanDistance(pos, ghostState.getPosition())
    		scared_distance.append(dist)
    	else:
    		#dealing here with the normal ghosts
    		dist = util.manhattanDistance(pos, ghostState.getPosition())
    		ghost_distance.append(dist)

	if len(scared_distance) != 0:
		score = score -  (4 * min(scared_distance))

    if len(ghost_distance) != 0:
    	if (min(ghost_distance) == 0):
    		score = -float('inf')
    	else:
    		score = score + (4 / min(ghost_distance))

    return score
    util.raiseNotDefined()
# Abbreviation
better = betterEvaluationFunction