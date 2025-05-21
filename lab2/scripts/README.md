# Coding Work #2 (Optional)

## HOWTOs
**Q: How to run the python code?**

**A:** You can use any PYTHON_ENV + IDE you preferred.
My recommendation is Anaconda + VSCODE/PyCharm


**Q: How to run this project?**

**A:** See below.

**Q: How to resolve "ModuleNotFoundError: No module named 'pygame'"**

**A:** You can use conda or pip to install this package. For example:
```bash
pip install conda
```
You can also install pygame via the Package Manager in Pycharm. 

**Q: How to start the search?**

**A:** After you see the GUI, just press 's'. You can also change the initial solution by assigning any cell you want'


----------------------------------------------------------------------
You can always run your code with the following command or add it to the configuration in your IDE
```bash
python main.py --partial_sol SUDOKU_PARTIAL_SOL --filtering YOUR_ALGOR --var VAR_MODE --value VAL_MODE
```

SUDOKU_PARTIAL_SOL is the partial solution of sudoku, you can choose:
```bash
part_sol_1
part_sol_2
```
You can find the definition of these partial solutions in directory "partial_sol"

YOUR_ALGOR is the arg of search method, you can choose:
```bash
forward_checking
ac1
ac3
ac4
```

For example, if you want to test your code with AC1, you can try:
```bash
python main.py --partial_sol part_sol_1 --filtering ac1 
```

It should be noted that you can use the heuristic function to choose the variable and value by adding "--var" and "--value"
For example:
```bash
python main.py --partial_sol part_sol_1 --filtering ac3 --var mrv --value lcv
```
where "MRV" and "LCV" are the functions to be implemented in "heuristics.py". You can also design your own heuristics in
this python file.

----------------------------------------------------------------------
Your task is to implement the undefined the functions in arc_consistency.py including:
```python
def ac3(problem):
    raiseNotDefined()


def ac4(problem):
    raiseNotDefined()

```
To start with the code, please read the implementations in "ac1".
AC1 can be very very slow!!! Therefore, you should write your own methods to make the search faster!

----------------------------------------------------------------------
You can also refer to "util.py" for useful functions and classes. For other functions and classes you want to add,
please always put them in "external_lib.py". DONT CHANGE OR WRITE YOUR CODES IN OTHER FILES.

The following files should be uploaded to CANVAS:
```bash
heuristics.py
arc_consistency.py
external_lib.py
```
----------------------------------------------------------------------
For any questions, feel free to contact with me and TAs.
We would like to thank the great efforts from UCB-CS188 teaching group. 

## GOOD LUCK AND HAVE FUN!


