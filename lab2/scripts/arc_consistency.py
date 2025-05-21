import util
from sudoku.csp_general import ConstraintSatisfactoryProblem
from sortedcontainers import SortedSet
from operator import eq, neg
from collections import defaultdict, Counter
from external_lib import *
from collections import defaultdict, deque
from queue import Queue


def no_arc_heuristic(csp, queue):
    return queue


def dom_j_up(csp:ConstraintSatisfactoryProblem, queue):
    return SortedSet(queue, key=lambda t: neg(len(csp.curr_domains[t[1]])))


def revise(csp, Xi, Xj, removals, checks=0):
    """Return true if we remove a value."""
    """对一条arc Xi->Xj的首尾进行约束验证,会检查Xi节点的每一个可能取值,只要有其中一个取值是要被舍弃的,就会返回True"""
    revised = False
    for x in csp.curr_domains[Xi]:
        # If Xi=x conflicts with Xj=y for every possible y, eliminate Xi=x
        # if all(not csp.constraints(Xi, x, Xj, y) for y in csp.curr_domains[Xj]):
        conflict = True
        for y in csp.curr_domains[Xj]: # 每次传到这里，Xj的curr_domains里不是只有一个值吗？？
            if csp.constraints(Xi, x, Xj, y): # 当节点Xi/Xj分别赋值x/y时，若符合约束则此函数返回True
                conflict = False
            checks += 1
            if not conflict:
                break # 只要Xj节点的取值中有一个是符合约束的，当前验证的Xi中的取值就是可以保留的，可以跳到Xi的下一个取值进行验证
        if conflict: # 如果Xj节点的每一个取值都违背约束，则Xi中的取值x要舍弃掉
            csp.prune(Xi, x, removals)
            revised = True
    return revised, checks


def ac1(csp, queue, removals=None, arc_heuristic=None): # queue的初始化为{(X, var) for X in csp.neighbors[var]}，是一个集合
    checks = 0
    while True:
        # print("Queue:", queue)  # 打印队列状态
        flag = False
        for Xi, Xj in queue: # 会检查所有与Xj连接的节点Xi
            revised, checks = revise(csp, Xi, Xj, removals, checks)
            if revised:
                if not csp.curr_domains[Xi]: # 如果在Xj定死为某个值的前提下，节点Xi所有的取值都验证失败
                    return False, checks  # 则此取值尝试中CSP is inconsistent, 回溯进行新尝试
            flag = flag or revised
        if not flag:
            break # repeat check until there's no deletion
    return True, checks


def ac3(csp, queue=None, removals=None, arc_heuristic=dom_j_up):
    # queue是一个集合，其中每个元素是一个元组
    checks = 0
    queue = list(queue) # 把queue从无需的集合类型转换为列表，后续作为队列使用
    while queue:
        # print("Queue:", queue)  # 打印队列状态
        Xi, Xj = util.first(queue)
        del(queue[0])
        revised, checks = revise(csp, Xi, Xj, removals, checks)
        if revised: 
            if not csp.curr_domains[Xi]: # 如果节点Xi所有取值都违背约束，返回False触发回溯
                return False, checks
            else: # 如果Xi中有取值被删掉了，就要在queue中添加以Xi为tail的所有arc
                for x in csp.neighbors[Xi]:   
                    if (x, Xi) not in queue: # 避免添加队列中已经存在的arc
                        queue.append((x, Xi)) 
    return True, checks

def ac4(csp, queue, removals=None, arc_heuristic=None):
    supports = defaultdict(set)       # 记录每个值的支持值
    counter = defaultdict(int)        # 记录每个值的有效约束计数
    processing_queue = deque()        # 用队列存储待处理的arc
    checks = 0                        # 约束检查次数

    for (Xi, Xj) in queue:
        for vi in csp.curr_domains.get(Xi, []):
            # 初始化计数器为0（假设当前值无支持）
            counter_key = (Xi, vi, Xj)
            counter[counter_key] = 0
            for vj in csp.curr_domains.get(Xj, []):
                checks += 1  # 统计约束检查次数
                if csp.constraints(Xi, vi, Xj, vj):
                    supports[(Xj, vj)].add((Xi, vi))
                    counter[counter_key] += 1
            # 如果当前值无支持，直接剪枝
            if counter[counter_key] == 0:
                csp.prune(Xi, vi, removals)
                processing_queue.append((Xi, vi))
                # 可行取值域为空时返回失败
                if not csp.curr_domains.get(Xi):
                    return False, checks

    while processing_queue:
        (Xi, vi) = processing_queue.popleft()
        # 遍历所有依赖当前值的支持值
        for (Xk, vk) in supports.get((Xi, vi), set()):
            # 更新计数器并检查是否失效
            key = (Xk, vk, Xi)
            counter[key] -= 1
            if counter[key] == 0:
                csp.prune(Xk, vk, removals)
                processing_queue.append((Xk, vk))
                # 可行取值域为空时返回失败
                if not csp.curr_domains.get(Xk):
                    return False, checks
        checks += 1

    return True, checks