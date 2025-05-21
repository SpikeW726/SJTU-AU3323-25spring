"""
    This is the file for your own classes and functions;
"""
import util
import heuristics


def search(problem, fringe, heuristic = heuristics.nullHeuristic):
    path = util.Path([problem.getStartState()], [], 0)
    if problem.isGoalState(problem.getStartState()):
        return []

    noCost = isinstance(fringe, util.Stack) or isinstance(fringe, util.Queue)
    if noCost:
        fringe.push(path)
    else:
        fringe.push(path, 0)

    visited = []

    while not fringe.isEmpty():
        current_path = fringe.pop()
        current_loc = current_path.locations[-1]
        if current_loc not in visited:
            visited.append(current_loc)
        else:
            continue
        if problem.isGoalState(current_loc):
            return current_path.actions
        else:
            successors = problem.getSuccessors(current_loc)
            for successor in successors:
                next_loc = successor[0]
                next_action = successor[1]
                next_cost = successor[2]
                if next_loc not in current_path.locations:
                    locations = current_path.locations[:]
                    locations.append(next_loc)
                    all_actions = current_path.actions[:]
                    all_actions.append(next_action)
                    next_cost = current_path.cost + next_cost
                    path = util.Path(locations, all_actions, next_cost)
                    if noCost:
                        fringe.push(path)
                    else:
                        fringe.push(path, next_cost + heuristic(next_loc, problem))

    return []





