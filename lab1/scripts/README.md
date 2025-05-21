# Coding Work #1

## HOWTOs
**Q: How to run the python code?**

**A:** You can use any PYTHON_ENV + IDE you preferred.
My recommendation is Anaconda + VSCODE/PyCharm


**Q: How to run this project?**

**A:** See below.

----------------------------------------------------------------------
You can always run your code with the following command or add it to the configuration in your IDE
```bash
python main.py -l MAP_NAME -p SearchAgent -a fn=YOUR_ALGOR
```

MAP_NAME is the testing map of pacman, you can choose:
```bash
tinyMaze
mediumMaze
```
You can find the definition of these maps in directory "layouts"

YOUR_ALGOR is the arg of search method, you can choose:
```bash
dfs
bfs
ucs
astar
```

For example, if you want to test your code with UCS, you can try:
```bash
python main.py -l tinyMaze -p SearchAgent -a fn=ucs
```

It should be noted that you can use the heuristic function for astar by adding "heuristic" as another argument.
For example:
```bash
python main.py -l mediumMaze -p SearchAgent -a fn=astar,heuristic=manhattanHeuristic
```
where "manhattanHeuristic" is the function implemented in "heuristics.py". You can also design your own heuristics in
this python file.

----------------------------------------------------------------------
Your task is to implement the undefined the functions in search_func.py including:
```python
def depthFirstSearch(problem):
    """Search the deepest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    raiseNotDefined()


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    raiseNotDefined()


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    raiseNotDefined()
```
To start with the code, please read the comments in "depthFirstSearch".

----------------------------------------------------------------------
You can also refer to "util.py" for useful functions and classes. For other functions and classes you want to add,
please always put them in "external_lib.py". DONT CHANGE OR WRITE YOUR CODES IN OTHER FILES.

The following files should be uploaded to CANVAS:
```bash
heuristics.py
search_func.py
external_lib.py
```
----------------------------------------------------------------------
For any questions, feel free to contact with me and TAs.
We would like to thank the great efforts from UCB-CS188 teaching group. 

## GOOD LUCK AND HAVE FUN!


