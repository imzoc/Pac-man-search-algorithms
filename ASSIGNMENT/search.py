# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

from util import *
import util


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do NOT need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:
    """
    i_state = problem.getStartState()

    visited = set()
    frontier = util.Stack()
    frontier.push(i_state)
    direction_map = {i_state: []}

    while not frontier.isEmpty():
        cur = frontier.pop()
        if problem.isGoalState(cur):
            return direction_map[cur]
        successors = problem.getSuccessors(cur)
        visited.add(cur)
        for successor, direction, _ in successors:
            if successor not in visited:
                frontier.push(successor)
                direction_map[successor] = direction_map[cur] + [direction]

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    i_state = problem.getStartState()

    visited = set()
    frontier = util.Queue()
    frontier.push(i_state)
    direction_map = {i_state: []}

    while not frontier.isEmpty():
        cur = frontier.pop()
        if problem.isGoalState(cur):
            return direction_map[cur]
        successors = problem.getSuccessors(cur)
        visited.add(cur) 
        for successor, direction, _ in successors:
            if successor not in visited and successor not in frontier.list:
                frontier.push(successor)
                direction_map[successor] = direction_map[cur] + [direction]    

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    i_state = problem.getStartState()

    visited = set()
    frontier = util.PriorityQueue()
    frontier.push(i_state, 0)
    direction_map = {i_state: []}
    cost_map = {i_state: 0}

    while not frontier.isEmpty():
        cur = frontier.pop()
        if problem.isGoalState(cur):
            return direction_map[cur]
        if cur in visited:
            continue
        successors = problem.getSuccessors(cur)
        visited.add(cur) 
        for successor, direction, cost in successors:
            if successor not in visited:
                if not any(successor == item for _, _, item in frontier.heap):
                    frontier.push(successor, cost_map[cur] + cost)
                    cost_map[successor] = cost_map[cur] + cost
                    direction_map[successor] = direction_map[cur] + [direction]    
                else:
                    if any(priority > cost_map[cur] + cost for priority, _, item in frontier.heap):
                        frontier.push(successor, cost_map[cur] + cost)
                        cost_map[successor] = cost_map[cur] + cost
                        direction_map[successor] = direction_map[cur] + [direction]    


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    
    i_state = problem.getStartState()

    class SearchNode:
        def __init__(self, state, g, h, directions):
            self.state = state
            self.g = g 
            self.h = h 
            self.f = g + h
            self.directions = directions

    closed = set()
    open = util.PriorityQueue()
    open.push(SearchNode(i_state, 0, 0, []), 0)
    
    while not open.isEmpty():
        cur = open.pop()
        if problem.isGoalState(cur.state):
            return cur.directions
        if any(cur.state == item.state for item in closed):
            continue
        closed.add(cur)
        for state, direction, cost in problem.getSuccessors(cur.state):
            g = cur.g + cost
            h = heuristic(state, problem)
            directions = cur.directions + [direction]
            successor = SearchNode(state, g, h, directions)

            if any(successor.state == item.state and successor.f >= item.f for _, _, item in open.heap) or\
                 any(successor.state == item.state and successor.f >= item.f for item in closed):
                continue

            open.push(successor, successor.f)


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
