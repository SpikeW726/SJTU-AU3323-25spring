import sys

from heuristics import *
from arc_consistency import no_arc_heuristic, ac3, ac4, ac1


def forward_checking(csp, var, value, assignment, removals):
    """Prune neighbor values inconsistent with var=value."""
    csp.support_pruning()
    for B in csp.neighbors[var]:
        if B not in assignment:
            for b in csp.curr_domains[B][:]:
                if not csp.constraints(var, value, B, b):
                    csp.prune(B, b, removals)
            if not csp.curr_domains[B]:
                return False
    return True


def mac(csp, var, value, assignment, removals, constraint_propagation=ac1):
    """Maintain arc consistency."""
    return constraint_propagation(csp, {(X, var) for X in csp.neighbors[var]}, removals)


def backtracking_search(csp, select_unassigned_variable=first_unassigned_variable,
                        order_domain_values=unordered_domain_values, inference=forward_checking):
    def backtrack(assignment):
        if len(assignment) == len(csp.variables):
            return assignment # 当assignment内元素数量等于variable数量时说明当前解法是满足约束的，直接返回
        var = select_unassigned_variable(assignment, csp)
        for value in order_domain_values(var, assignment, csp):
            if csp.nconflicts(var, value, assignment) == 0:
                csp.assign(var, value, assignment)
                removals = csp.suppose(var, value)
                if inference(csp, var, value, assignment, removals):
                    result = backtrack(assignment)
                    if result is not None:
                        return result
                csp.restore(removals)
        csp.unassign(var, assignment)
        return None

    result = backtrack({}) # assignment是个词典，初始状态为空
    assert result is None or csp.goal_test(result)
    return result


def backtracking_wrapper(csp, opt):
    if opt['var'] == 'mrv':
        var = mrv
        print('Variable Ordering with: MRV')
    elif opt['var'] == 'next':
        var = first_unassigned_variable
        print('Variable Ordering with: Next Unassigned')
    else:
        print('Variable Ordering Strategy [%s] is Unknown!' % opt['var'])
        sys.exit(1)

    if opt['value'] == 'lcv':
        value = lcv
        print('Value Ordering with: LeastConstraints')
    elif opt['value'] == 'random':
        value = unordered_domain_values
        print('Value Ordering with: Random')
    else:
        print('Value Ordering Strategy [%s] is Unknown!' % opt['value'])
        sys.exit(1)

    if opt['filtering'] == 'forward_checking':
        inference = forward_checking
        print('Filtering with: Forward Checking Only')

    elif opt['filtering'] == 'ac1':
        inference = lambda _csp, _var, _value, _assignment, _removals: \
            mac(_csp, _var, _value, _assignment, _removals, ac1)
        print('Filtering with: AC1')

    elif opt['filtering'] == 'ac3':
        inference = lambda _csp, _var, _value, _assignment, _removals: \
            mac(_csp, _var, _value, _assignment, _removals, ac3)
        print('Filtering with: AC3')

    elif opt['filtering'] == 'ac4':
        inference = lambda _csp, _var, _value, _assignment, _removals: \
            mac(_csp, _var, _value, _assignment, _removals, ac4)
        print('Filtering with: AC4')

    else:
        print('Filtering Strategy [%s] is Unknown!' % opt['filtering'])
        sys.exit(1)
    # 根据解析命令行得到的内容确定传入backtracking_search的ordering和filtering函数
    return backtracking_search(csp, var, value, inference)
