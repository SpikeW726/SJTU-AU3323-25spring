from pacman.game import Directions
from pacman.util import raiseNotDefined
import util
from heuristics import nullHeuristic, manhattanHeuristic2
import external_lib


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem, max_depth=-1):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Are we reaching a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))

    You can also refer to the function "tinyMazeSearch"
    """
    "*** YOUR CODE HERE ***"
    # print("Start:", problem.getStartState())
    # print("Are we reaching a goal?", problem.isGoalState(problem.getStartState()))
    # print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    path = util.Path([problem.getStartState()],[],0)     
    fringe = util.Stack()
    fringe.push(path)
    
    while not fringe.isEmpty():
        
        current_path = fringe.pop()
        current_node = current_path.locations[-1]
        
        if problem.isGoalState(current_node): return current_path.actions
        for successor in problem.getSuccessors(current_node):
            if successor[0] not in current_path.locations:
                current_nodes = current_path.locations[:]
                current_nodes.append(successor[0])
                current_actions = current_path.actions[:]
                current_actions.append(successor[1])
                current_cost = current_path.cost + successor[2]
                path = util.Path(current_nodes, current_actions, current_cost)
                fringe.push(path)
    
    return []
    # raiseNotDefined()  # DONT FORGET TO COMMENT THIS LINE AFTER YOU IMPLEMENT THIS FUNCTION!!!!!!


def breadthFirstSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    path = util.Path([problem.getStartState()],[],0)
    visited = {problem.getStartState():True} # 用来存储访问过的节点
    fringe = util.Queue()
    fringe.push(path)
    
    while not fringe.isEmpty():
        
        current_path = fringe.pop()
        current_node = current_path.locations[-1]
        
        if problem.isGoalState(current_node): return current_path.actions
        for successor in problem.getSuccessors(current_node):
            if not visited.get(successor[0], False):
                visited[successor[0]] = True
                current_nodes = current_path.locations[:]
                current_nodes.append(successor[0])
                current_actions = current_path.actions[:]
                current_actions.append(successor[1])
                current_cost = current_path.cost + successor[2]
                path = util.Path(current_nodes, current_actions, current_cost)
                fringe.push(path)
    
    return []
    # raiseNotDefined()  # DONT FORGET TO COMMENT THIS LINE AFTER YOU IMPLEMENT THIS FUNCTION!!!!!!


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    start = problem.getStartState()
    path = util.Path([start],[],0)
    minCost = {start:0}   # 记录每个节点最小的代价，只有当新路径的代价更小或探索到新节点时才会更新   
    fringe = util.PriorityQueue()
    fringe.push(path, path.cost)
    
    while not fringe.isEmpty():
        
        current_path = fringe.pop()
        current_node = current_path.locations[-1]
        current_cost = current_path.cost

        if problem.isGoalState(current_node): return current_path.actions
        else:
            for successor in problem.getSuccessors(current_node):
                new_node = successor[0]
                new_action = successor[1]
                new_cost = current_cost + successor[2]

                if new_node not in minCost or new_cost < minCost[new_node]:
                    minCost[new_node] = new_cost
                    new_nodes = current_path.locations[:]
                    new_nodes.append(new_node)
                    new_actions = current_path.actions[:]
                    new_actions.append(new_action)
                    path = util.Path(new_nodes, new_actions, new_cost)
                    fringe.push(path,path.cost)
    
    return []
    # raiseNotDefined()  # DONT FORGET TO COMMENT THIS LINE AFTER YOU IMPLEMENT THIS FUNCTION!!!!!!



def aStarSearch(problem, heuristic=manhattanHeuristic2):
    """Search the node that has the lowest combined cost and heuristic first."""
    start = problem.getStartState()
    init_g = 0
    init_h = heuristic(start, problem)
    path = util.Path([start],[],init_g)
    # 记录每个节点最小的代价，保证到当前节点的路径是实际cost最小的
    minCost = {problem.getStartState():0}
    fringe = util.PriorityQueue()
    fringe.push(path, init_g+init_h)
    
    while not fringe.isEmpty():
        
        current_path = fringe.pop()
        current_node = current_path.locations[-1]
        current_g = current_path.cost

        if problem.isGoalState(current_node): return current_path.actions
        for successor in problem.getSuccessors(current_node):
            new_node = successor[0]
            new_action = successor[1]
            new_g = current_g + successor[2]
            new_h = heuristic(new_node, problem)

            if new_node not in minCost or new_g < minCost[new_node]:
                minCost[new_node] = new_g
                new_nodes = current_path.locations[:]
                new_nodes.append(new_node)
                new_actions = current_path.actions[:]
                new_actions.append(new_action)
                path = util.Path(new_nodes, new_actions, new_g)
                fringe.push(path,new_g+new_h)
    
    return []

    # raiseNotDefined()  # DONT FORGET TO COMMENT THIS LINE AFTER YOU IMPLEMENT THIS FUNCTION!!!!!!


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
