import util
from util import first, count, argmin_random_tie
from external_lib import *



def num_legal_values(csp, var, assignment):
    if csp.curr_domains:
        return len(csp.curr_domains[var])
    else:
        return count(csp.nconflicts(var, val, assignment) == 0 for val in csp.domains[var])


# Variable Ordering
def first_unassigned_variable(assignment, csp):
    """The default variable order."""
    return first([var for var in csp.variables if var not in assignment])


def mrv(assignment, csp):
    """Minimum-remaining-values heuristic."""
    # 在backtracking_search函数调用mrv函数前，csp.curr_domains还是None，所以此处要先初始化一下
    csp.support_pruning()
    min_domain = float("inf")
    # 遍历找出可行取值域最小的节点
    for var in csp.variables:
        if var not in assignment:
            if len(csp.curr_domains[var]) < min_domain:
                min_domain = len(csp.curr_domains[var])                
                target_var = var
    return target_var


# Value ordering
def unordered_domain_values(var, assignment, csp):
    """The default value order."""
    return csp.choices(var) # Return all values for var that aren't currently ruled out.


def lcv(var, assignment, csp):
    """Least-constraining-values heuristic."""
    csp.support_pruning()
    dict = {} # 构建一个字典，键为var的可行取值，值为给var分配键对应的值时需要prune的次数
    for val in csp.curr_domains[var]:
        tmp_prune_cnt = 0
        csp.assign(var, val, assignment)
        for var_neighbor in csp.neighbors[var]:
            for val_neighbor in csp.curr_domains[var_neighbor]:
                '''
                nconflit函数检测当var_neighbor取val_neighbor时，与其neighbor节点中【已经assign了值】的var冲突的个数
                而在这里只有var时assign了值的，所以相当于检查var_neighbor取val_neighbor是否与var取value冲突
                若冲突tmp_prune_cnt值+1，若不冲突tmp_prune_cnt值不变
                '''
                tmp_prune_cnt += csp.nconflicts(var_neighbor, val_neighbor, assignment)
        dict[val] = tmp_prune_cnt
    # 按照dict中值的大小排序，返回键的升序队列
    sorted_keys = sorted(dict, key=lambda k: dict[k])
    return sorted_keys
        





